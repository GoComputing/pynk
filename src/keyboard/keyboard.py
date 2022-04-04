from adafruit_hid.keyboard import Keycode
from keyboard import hid
import time



class Keyboard:
    
    def __init__(self, cfg):

        self.model = cfg['model']
        self.micro = cfg['micro']
        self.hid = hid.HID(cfg['device_info'])
    
    
    def __str__(self):
        
        return 'Model ({}), Microcontroller ({})'.format(
            self.model,
            self.micro
        )
    
    
    def loop(self):
        
        while True:
            time.sleep(1)
            # self.hid.send(Keycode.A)
