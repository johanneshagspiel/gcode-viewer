import json
from pathlib import Path

from gcode_viewer.util.mapper_util import Mapper_Util


class File_Handler():

    def __init__(self):
        self.root = Path.joinpath(Path(__file__).parents[1], "resources")

        self.gcode_path = Path.joinpath(self.root, "string_list")
        self.font_path = Path.joinpath(self.root, "fonts")
        self.icon_path = Path.joinpath(self.root, "icons")
        self.settings_path = Path.joinpath(self.root, "settings")

        self.icon_ico_path = Path.joinpath(self.icon_path, "apple_icon.ico")
        self.icon_png_path = Path.joinpath(self.icon_path, "apple_icon.png")
        self.used_font_path = Path.joinpath(self.font_path, "Eurostile LT Std.otf")

        self.diameter_1_5_path = Path.joinpath(self.gcode_path, "1.5")
        self.diameter_0_8_path = Path.joinpath(self.gcode_path, "0.8")
        self.diameter_0_6_path = Path.joinpath(self.gcode_path, "0.6")

        self.settings_file_path = Path.joinpath(self.settings_path, "settings_file.json")

    def read_gcode_file(self, file_path):
        line_list = []
        with open(file_path, 'r') as f:
            line_list = [line.strip() for line in f if line.strip()]

        return line_list

    # def write_file(self, string_list: GCode, path, file_name):
    #     file_name_extension = file_name + ".string_list"
    #     file_path = Path.joinpath(Path(path), file_name_extension)
    #
    #     f = open(file_path, "w")
    #     f.write(string_list.whole_code)
    #     f.close()

    def read_settings(self):

        with open(self.settings_file_path) as file:
            new_settings_json = json.loads(file.read())

        new_settings = Mapper_Util.json_to_settings(new_settings_json)
        return new_settings

    def settings_to_file(self, settings):

        settings_json = Mapper_Util.settings_to_json(settings)

        with open(self.settings_file_path, "w") as file:
            file.write(json.dumps(settings_json))
            file.close()