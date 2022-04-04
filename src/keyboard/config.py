import json
import os


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
