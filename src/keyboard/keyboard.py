from adafruit_hid.keyboard import Keycode
from keyboard import hid, matrix, layout
import time


def load_keyboard_model(keyboard_name):
    
    # Get the library that manages a certain keyboard (keyboard_handler)
    try:
        module = __import__('models.'+keyboard_name)
        keyboard_model = getattr(module, keyboard_name)
    except:
        raise ValueError('Keyboard not found ({})'.format(keyboard_name))
    
    return keyboard_model


def load_layout(layout_name, pc_layout_name, keyboard_model):
    
    # Get some parameters
    nrows = keyboard_model.config.NROWS
    ncols = keyboard_model.config.NCOLS
    
    # Get the layout
    return layout.Layout(nrows, ncols, layout_name, pc_layout_name)




class Keyboard:
    
    def __init__(self, cfg):

        # Parse config
        self.name = cfg['model']
        self.micro = cfg['micro']
        self.selected_part = cfg['selected_part']
        self.part_cfg = cfg['parts'][self.selected_part]
        self.rol = self.part_cfg['rol']
        
        # Create handlers
        self.hid = hid.get_hid(self.part_cfg)
        self.model = load_keyboard_model(self.name)
        self.matrix = matrix.Matrix(self.model, self.micro, self.selected_part)
        
        # Specific master handlers
        if self.rol == 'master':
            self.layout_name = cfg['layout']
            self.pc_layout_name = cfg['pc_layout']
            self.layout = load_layout(self.layout_name, self.pc_layout_name, self.model)
            self.layer_0 = False
            self.layer_1 = False
            
            # Find the slave part (if any)
            slave_part = None
            slave_name = None
            for part_name, part_cfg in cfg['parts'].items():
                if part_cfg['rol'] == 'slave':
                    slave_part = part_cfg
                    slave_name = part_name
                    break
            self.slave_name = None
            if slave_name is not None:
                self.slave_part = {
                    'name' : slave_name,
                    'cfg' : slave_part
                }
    
    
    def start(self):
        
        self.hid.start()
        self.receiver = None
        if self.rol == 'master' and self.slave_part is not None:
            self.receiver = hid.get_receiver(self.slave_part['name'], self.slave_part['cfg'])
            self.receiver.start()
    
    
    def __str__(self):
        
        return 'Model ({}), Microcontroller ({})'.format(
            self.name,
            self.micro
        )
    
    def get_current_layer(self):
        """ Should only be called from master """
        
        return (int(self.layer_1) << 1) | int(self.layer_0)
    
    def update_events(self, timeout):
        
        # Read the events
        n = self.matrix.wait(timeout=timeout)
        events = [(self.matrix.get(), self.selected_part) for _ in range(n)]
        
        # Process the events if we are the master
        if self.rol == 'master':
            
            # Receive slave elements and add them to 'events'
            if self.receiver is not None:
                events = events + [event for event in self.receiver.read_events()]
            
            # Transform key positions to final keycodes
            keypos2rowcol = self.model.config.keypos2rowcol
            final_events = []
            for event in events:
                
                keypos = event[0][0]
                release = event[0][1]
                selected_part = event[1]
                current_layer = self.get_current_layer()
                
                row, col = keypos2rowcol(keypos, selected_part)
                keycodes, is_macro = self.layout.get_keycode(row, col, current_layer)
                
                # Two kind of keys: normal keys and macro keys
                # Normal keys are sent directly to the PC
                # Macro keys are special keys with different functions (for example, layout selection, led control, etc)
                if is_macro:
                    # TODO: Update self.layer_0 and self.layer_1
                    # [...]
                    pass
                else:
                    final_events.append((keycodes, release))
        elif self.rol == 'slave':
            final_events = [([event[0][0]], event[0][1]) for event in events]
        
        return final_events
            
            
    
    
    def loop(self):
        
        matrix = self.matrix
        
        while self.hid.is_connected():
            
            events = self.update_events(timeout=5)
            
            keypresses  = [keycodes for keycodes,release in events if not release]
            keyreleases = [keycodes for keycodes,release in events if release]
            
            for keycodes in keypresses:
                self.hid.press(keycodes)
            for keycodes in keyreleases:
                self.hid.release(keycodes)
        
        print("Connection lost (did you call keyboard.start?)")
