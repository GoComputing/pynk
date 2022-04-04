import json
import time
import os


###############################
# Parameters
###############################

CONFIG_PATH = "config.json"






###############################
# Helpers
###############################

# TODO
def config_check(cfg, raise_except):
    
    # Config sintax
    cfg_schema = {
        'type': 'object',
        'properties': {
            'model' : { 'type' : 'string' },
            'micro' : { 'type' : 'string' }
        }
    }

def read_config(path):
    
    # Config read
    with open(path, "r") as f:
        raw_content = ''.join(f.readlines())
    cfg = json.loads(raw_content)
    
    # Config syntax check
    config_check(cfg, raise_except=True)
    
    return cfg






###############################
# Keyboard class
###############################

class Keyboard:
    
    def __init__(self, cfg):

        self.model = cfg['model']
        self.micro = cfg['micro']
    
    
    def __str__(self):
        
        return 'Model ({}), Microcontroller ({})'.format(
            self.model,
            self.micro
        )
    
    
    def loop(self):
        
        while True:
            time.sleep(0.1)






###############################
# Main
###############################

def main():
    
    # Read config
    cfg = read_config(CONFIG_PATH)
    
    # Initialize keyboard and all its modules
    keyboard = Keyboard(cfg)
    print(keyboard)

    # Keyboard loop
    keyboard.loop()


if __name__ == '__main__':
    main()
