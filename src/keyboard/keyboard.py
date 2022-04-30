from adafruit_hid.keyboard import Keycode
from keyboard import hid, matrix
import time



class Keyboard:
    
    def __init__(self, cfg):

        self.model = cfg['model']
        self.micro = cfg['micro']
        self.selected_part = cfg['selected_part']
        self.hid = hid.HID(cfg['parts'][self.selected_part])
        self.matrix = matrix.Matrix(self.model, self.micro, self.selected_part)
    
    
    def __str__(self):
        
        return 'Model ({}), Microcontroller ({})'.format(
            self.model,
            self.micro
        )
    
    def _read_event(self):
        
        # Read the event (assume there is event)
        key = self.matrix.get()
        release = bool(key & 0x80)
        if release:
            key = key & 0x7F
        
        return (key, release)
    
    def update_events(self, timeout):
        
        n = self.matrix.wait(timeout=timeout)
        events = [self._read_event() for _ in range(n)]
        
        return events
            
            
    
    
    def loop(self):
        
        matrix = self.matrix
        
        while True:
            
            events = self.update_events(timeout=1000)
            
            for event in events:
                print(event, end=' ')
            if len(events) > 0:
                print()
            # self.hid.send(Keycode.A)
