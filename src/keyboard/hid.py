from adafruit_hid.keyboard import Keyboard

class HID:
    
    def __init__(self, device_info):
        """
        Supported connection types
         * usb (master)
         * ble (master) [TODO]
        """
        
        conn_type = device_info['connection']
        
        if conn_type == 'usb':
            import usb_hid
            self.hid = Keyboard(usb_hid.devices)
        else:
            raise ValueError('Invalid connection type ({})'.format(conn_type))
    
    
    def is_connected(self):
        pass
    
    def send(self, *keys):
        self.hid.send(*keys)
    
    def press(self, *keys):
        self.hid.press(*keys)
    
    def release(self, *keys):
        self.hid.release(*keys)
    
    def release_all(self):
        self.hid.release_all()
