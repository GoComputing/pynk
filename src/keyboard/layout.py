import json


def gen_keycodes(layer, pc_layout_name):
    
    # Load the layout
    with open('/pc_layouts/{}.json'.format(pc_layout_name), 'r') as f:
        raw_content = ''.join(f.readlines())
        pc_layout = json.loads(raw_content)
    
    # Translate the keys to keycodes
    for row in layer:
        for i in range(len(row)):
            if row[i] in pc_layout:
                keycodes = [int(keycode) for keycode in pc_layout[row[i]]]
                row[i] = (keycodes, False) # Keycode, is_macro
            else:
                row[i] = (row[i], True) # Keycode, is_macro

def gen_keycodes_layers(layers, pc_layout_name):
    
    for _,layer in layers.items():
        gen_keycodes(layer, pc_layout_name)


class Layout:

    def __init__(self, nrows, ncols, layout_name, pc_layout_name):
        
        self.nrows = nrows
        self.ncols = ncols
        
        self.set_layout(layout_name, pc_layout_name)

    
    def set_layout(self, layout_name, pc_layout_name):
        
        self.layout_name = layout_name
        self.pc_layout_name = pc_layout_name
        
        layout_path = '/layouts/{}_{}x{}.txt'.format(layout_name, self.nrows, self.ncols)
        
        self.layers = dict()
        self.layers_order = []
        
        with open(layout_path, 'r') as f:
            
            reading_name = True
            layer = []
            for line in f.readlines():
                
                line = line.strip()
                if len(line) > 0:
                    
                    if reading_name:
                        layer_name = line
                        reading_name = False
                    else:
                        row = line.split()
                        layer.append(row)
                        
                        if len(layer) == self.nrows:
                            self.layers[layer_name] = layer
                            self.layers_order.append(layer_name)
                            layer = []
                            reading_name = True
        
        gen_keycodes_layers(self.layers, pc_layout_name)
    
    
    def get_keycode(self, row, col, current_layer):
        
        # TODO: Keep pressed keycodes so the release is not affected by the layer selection
        # Ej: K key is pressed. Then the user change the layer. Then the user release K key
        # The release keycode would not be the same as the pressed keycode
        
        key = self.layers[self.layers_order[current_layer]][row][col]
        keycodes = key[0]
        is_macro = key[1]
        
        return keycodes, is_macro
    
