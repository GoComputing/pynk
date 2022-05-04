from keyboard.keyboard import Keyboard
from keyboard.config import read_config


###############################
# Parameters
###############################

CONFIG_PATH = "config.json"






###############################
# Main
###############################

def main():
    
    # Read config
    cfg = read_config(CONFIG_PATH)
    
    # Initialize keyboard and all its modules
    keyboard = Keyboard(cfg)
    print(keyboard)
    
    # Start connections and other stuff
    keyboard.start()

    # Keyboard loop
    keyboard.loop()


if __name__ == '__main__':
    main()
