import digitalio
import time



# This code is mostly based on 'https://github.com/makerdiary/python-keyboard/blob/main/keyboard/matrix.py'




def set_pin_as_input(pin, row2col):
    
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.DOWN if row2col else digitalio.Pull.UP
    return io

def set_pin_as_output(pin):
    
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.OUTPUT
    io.drive_mode = digitalio.DriveMode.PUSH_PULL
    io.value = 0
    return io



class Matrix:
    
    def __init__(self, keyboard_model, microcontroller_name, selected_part):
        
        # Get the library that manages a certain keyboard (keyboard_handler)
        try:
            module = __import__('models.'+keyboard_model)
            keyboard_handler = getattr(module, keyboard_model)
        except:
            raise ValueError('Keyboard not found ({})'.format(keyboard_model))
        
        # Get pin numbers (and so the number of rows and columns)
        self.row_pins, self.col_pins = keyboard_handler.pins.get_keyboard_pins(microcontroller_name, selected_part)
        
        # Initialize the pins
        self.row2col = keyboard_handler.pins.is_row2col(selected_part)
        self.rows = [set_pin_as_output(pin) for pin in self.row_pins]
        self.cols = [set_pin_as_input(pin, self.row2col) for pin in self.col_pins]
        
        # Initialize state variables
        self.keys = len(self.rows) * len(self.cols)
        self.pressed = bool(self.row2col)
        self.t0 = [0] * self.keys  # key pressed time
        self.t1 = [0] * self.keys  # key released time
        self.mask = 0
        self.count = 0
        self._debounce_time = 20000000
        self.length = 0
        self.queue = bytearray(self.keys)
        self.head = 0
        self.tail = 0
    
    
    def scan(self):
        """
        Scan keyboard matrix and save key event into the queue.
        :return: length of the key event queue.
        """
        t = time.monotonic_ns()

        # use local variables to speed up
        pressed = self.pressed
        last_mask = self.mask
        cols = self.cols

        mask = 0
        count = 0
        key_index = -1
        for row in self.rows:
            row.value = pressed  # select row
            for col in cols:
                key_index += 1
                if col.value == pressed:
                    key_mask = 1 << key_index
                    if not (last_mask & key_mask):
                        if t - self.t1[key_index] < self._debounce_time:
                            continue

                        self.t0[key_index] = t
                        self.put(key_index)

                    mask |= key_mask
                    count += 1
                elif last_mask and (last_mask & (1 << key_index)):
                    if t - self.t0[key_index] < self._debounce_time:
                        mask |= 1 << key_index
                        continue

                    self.t1[key_index] = t
                    self.put(0x80 | key_index)

            row.value = not pressed
        self.mask = mask
        self.count = count

        return self.length

    def wait(self, timeout=1000):
        """Wait for a new key event or timeout (ms)"""
        last = self.length
        if timeout:
            end_time = time.monotonic_ns() + timeout * 1000000
            while True:
                n = self.scan()
                if n > last or time.monotonic_ns() > end_time:
                    return n
        else:
            while True:
                n = self.scan()
                if n > last:
                    return n

    def put(self, data):
        """Put a key event into the queue"""
        self.queue[self.head] = data
        self.head += 1
        if self.head >= self.keys:
            self.head = 0
        self.length += 1

    def get(self):
        """Remove and return the first event from the queue."""
        data = self.queue[self.tail]
        self.tail += 1
        if self.tail >= self.keys:
            self.tail = 0
        self.length -= 1
        return data

    def view(self, n):
        """Return the specified event"""
        return self.queue[(self.tail + n) % self.keys]

    def __getitem__(self, n):
        """Return the specified event"""
        return self.queue[(self.tail + n) % self.keys]

    def __len__(self):
        """Return the number of events in the queue"""
        return self.length

    def get_keydown_time(self, key):
        """Return the key pressed time"""
        return self.t0[key]

    def get_keyup_time(self, key):
        """Return the key released time"""
        return self.t1[key]

    def time(self):
        """Return current time"""
        return time.monotonic_ns()

    def ms(self, t):
        """Convert time to milliseconds"""
        return t // 1000000
