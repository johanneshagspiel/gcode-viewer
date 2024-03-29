from gcode_viewer.gcode.layer import Layer


class Layer_Parser():

    def __init__(self):
        None

    def parse_layer_list(self, string_list):

        self.last_z_value = 0
        self.from_x = 0
        self.from_y = 0
        self.from_z = 0

        self.to_x = 0
        self.to_y = 0
        self.to_z = 0

        self.min_x = 1000000000000000000000000
        self.max_x = 0
        self.min_y = 1000000000000000000000000
        self.max_y = 0

        split_into_layers_list = self.split_into_layers(string_list)

        parsed_layer_list = []

        for layer in split_into_layers_list:
            parsed_layer_list.append(self.parse_single_layer(layer))

        return parsed_layer_list

    def split_into_layers(self, list_to_split):

        result_list = []
        current_layer = []

        for line in list_to_split:
            if ";TIME_ELAPSED:" in line:
                current_layer.append(line)
                result_list.append(current_layer)
                current_layer = []
            else:
                current_layer.append(line)

        return result_list

    def parse_single_layer(self, string_to_be_parsed):
        layer = Layer()

        layer.layer_as_string = string_to_be_parsed

        movement_commands = ["G0", "G1", "G2", "G3", "G5"]
        largest_extrusion_value = 0

        for index, line in enumerate(string_to_be_parsed):
            if ";" in line[0]:
                if "LAYER:" in line:
                    layer_number = line.split(":")[1]
                    layer.number = int(layer_number)
            else:
                self.from_x = self.to_x
                self.from_y = self.to_y
                self.from_z = self.to_z

                split_line = line.split()
                if split_line[0] in movement_commands:
                    if "G1" in line:
                        layer.pyqtgraph_color.append((1., 1., 1., 0.))
                        layer.matplot_color.append(("r"))
                    if "G0" in line:
                        layer.pyqtgraph_color.append((1., 1., 1., 0.))
                        layer.matplot_color.append(("b"))
                    split_line = line.split()
                    for word in split_line:
                        if "E" in word:
                            extrusion_value = float(word[1:])
                            if extrusion_value > largest_extrusion_value:
                                largest_extrusion_value = extrusion_value
                        if "X" in word:
                            x_position = float(word[1:])
                            self.to_x = x_position
                        if "Y" in word:
                            y_position = float(word[1:])
                            self.to_y = y_position
                        if "Z" in word:
                            z_position = float(word[1:])
                            self.to_z = z_position
                else:
                    layer.pyqtgraph_color.append((1., 1., 1.))
                    layer.matplot_color.append(("g"))

                layer.x_data.append((self.from_x, self.to_x))
                layer.y_data.append((self.from_y, self.to_y))
                layer.z_data.append((self.from_z, self.to_z))
                layer.move_data.append(line)

                self.update_min_max()

        layer.min_x = self.min_x - 2.5
        layer.max_x = self.max_x + 2.5
        layer.min_y = self.min_y - 2.5
        layer.max_y = self.max_y + 2.5

        self.min_x = 1000000000000000000000000
        self.max_x = 0
        self.min_y = 1000000000000000000000000
        self.max_y = 0

        layer.largest_extrusion_value = largest_extrusion_value

        return layer

    def update_min_max(self):

        larger_x = 0
        smaller_x = 0

        if self.to_x > self.from_x:
            larger_x = self.to_x
            smaller_x = self.from_x
        else:
            larger_x = self.from_x
            smaller_x = self.to_x

        if larger_x > self.max_x:
            self.max_x = larger_x
        if smaller_x < self.min_x:
            self.min_x = smaller_x

        larger_y = 0
        smaller_y = 0

        if self.to_y > self.from_y:
            larger_y = self.to_y
            smaller_y = self.from_y
        else:
            larger_y = self.from_y
            smaller_y = self.to_y

        if larger_y > self.max_y:
            self.max_y = larger_y
        if smaller_y < self.min_y:
            self.min_y = smaller_y