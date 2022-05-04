from adafruit_hid.keyboard import Keyboard

class USB_hid:
    
    def __init__(self):
        import usb_hid
        self.hid = Keyboard(usb_hid.devices)
    
    def start(self):
        # TODO (?) Does it make sense to start USB hid?
        pass
    
    def is_connected(self):
        # TODO (?) Does it make sense to check if the USB is connected?
        return True
    
    def send(self, keys):
        self.hid.send(*keys)
    
    def press(self, keys):
        self.hid.press(*keys)
    
    def release(self, keys):
        self.hid.release(*keys)
    
    def release_all(self):
        self.hid.release_all()







def change_uartservice_timeout(uartservice_class, timeout):
    uartservice_class._server_rx._timeout = timeout
    uartservice_class._server_tx._timeout = timeout

# Package format:
#  * Length: 1 byte
#  * 1xxxxxxx -> Key package
#  * 0xxxxxxx -> Reserved

# Key package
#  * 11xxxxxx -> Key press
#  * 10xxxxxx -> Key releas
#  * The key is coded in the first 6 bits of the package


BLE_INTERNAL_KEY_FLAG      = 0x80
BLE_INTERNAL_KEYPRESS_FLAG = 0x40

BLE_INTERNAL_KEYPRESS   = (0xC0, 0x3F)
BLE_INTERNAL_KEYRELEASE = (0x80, 0x3F)


class BLE_internal:
    
    def __init__(self, timeout=0):
        
        from adafruit_ble import BLERadio
        from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
        from adafruit_ble.services.nordic import UARTService
        
        change_uartservice_timeout(UARTService, timeout)
        
        self.ble = BLERadio()
        self.uart = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart)
    
    def _send_pkg(self, pkg_meta, payload):
        pkg_id = pkg_meta[0]
        pkg_len = pkg_meta[1]
        package = pkg_id | (payload & pkg_len)
        self.uart.write(package.to_bytes(1, 'little'))
    
    def start(self):
        
        self.ble.start_advertising(self.advertisement)
        print("Connecting to master...")
        while not self.ble.connected:
            pass
        print("Connected!")
    
    def is_connected(self):
        
        return self.ble.connected
    
    def send(self, keys):
        """ This method should only be called from master """
        
        raise NotImplementedError
    
    def press(self, keys):
        
        for key in keys:
            self._send_pkg(BLE_INTERNAL_KEYPRESS, key)
    
    def release(self, keys):
        
        for key in keys:
            self._send_pkg(BLE_INTERNAL_KEYRELEASE, key)
    
    def release_all(self):
        raise NotImplementedError
    
    




def get_hid(device_info):
    """
    Supported connection types
     * usb (master)
     * ble (master) [TODO]
     * ble (slave) [TODO]
    """
    
    conn_type = device_info['connection_type']
    rol = device_info['rol']
    
    if conn_type == 'usb':
        if rol != 'master':
            raise ValueError('USB connection is only supported in the master node')
        
        hid = USB_hid()
    elif conn_type == 'ble':
        if rol == 'master':
            # TODO
            pass
        elif rol == 'slave':
            hid = BLE_internal()
    else:
        raise ValueError('Invalid connection type ({})'.format(conn_type))
    
    return hid









class BLE_receiver:
    
    def __init__(self, slave_name, timeout=0):
        
        from adafruit_ble import BLERadio
        from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
        from adafruit_ble.services.nordic import UARTService
        
        change_uartservice_timeout(UARTService, timeout)
        
        self.BLERadio = BLERadio
        self.ProvideServicesAdvertisement = ProvideServicesAdvertisement
        self.UARTService = UARTService
        
        self.ble = BLERadio()
        self.slave_name = slave_name
    
    
    def _read_pkg(self):
        
        payload = None
        pkg_id = None
        
        if self.ble.connected:
            uart = self.connection[self.UARTService]
            package = uart.read(1)
            
            if len(package) > 0:
                package = package[0]
                if package & BLE_INTERNAL_KEY_FLAG:
                    if package & BLE_INTERNAL_KEYPRESS_FLAG:
                        pkg_id = BLE_INTERNAL_KEYPRESS[0]
                        payload = package & BLE_INTERNAL_KEYPRESS[1]
                    else:
                        pkg_id = BLE_INTERNAL_KEYRELEASE[0]
                        payload = package & BLE_INTERNAL_KEYRELEASE[1]
                else:
                    raise ValueError("Invalid package")
        
        return pkg_id, payload
    
    
    def start(self):
        
        while not self.ble.connected:
            
            print("Waiting for slave part")
            
            for advertisement in self.ble.start_scan(self.ProvideServicesAdvertisement, timeout=1):
                if self.UARTService not in advertisement.services:
                    continue
                self.connection = self.ble.connect(advertisement)
                print("Connected!")
                break
            self.ble.stop_scan()

    def is_connected(self):
        
        return self.ble.connected
    
    def read_event(self):
        
        # Event structure:
        # ((keypos, release), part_name)
        
        event = None
        pkg_id, payload = self._read_pkg()
        
        if pkg_id is not None:
            if pkg_id == BLE_INTERNAL_KEYPRESS[0]:
                event = ((payload, False), self.slave_name)
            elif pkg_id == BLE_INTERNAL_KEYRELEASE[0]:
                event = ((payload, True), self.slave_name)
            else:
                # TODO
                raise NotImplementedError("Package type processing not implemented")
        
        return event
    
    def read_events(self, max_events=16):
        
        new_events = True
        events = []
        while len(events) < max_events and new_events:
            
            event = self.read_event()
            if event is None:
                new_events = False
            else:
                events.append(event)
        
        return events




def get_receiver(device_name, device_info):
    
    """
    Supported connection types
     * ble
    """
    
    conn_type = device_info['connection_type']
    
    if conn_type == 'ble':
        receiver = BLE_receiver(device_name)
    else:
        raise ValueError('Invalid receiver type ({})'.format(conn_type))
    
    return receiver
