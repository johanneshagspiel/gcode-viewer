from gcode_viewer.util.settings import Printer, Sponge, Environment, Settings


class Mapper_Util():

    def __init__(self):
        None

    @staticmethod
    def json_to_settings(json):
        environment_json = json['environment']
        printer_json = environment_json['printer']
        new_printer = Printer(printer_json['bed_width_x'], printer_json['bed_depth_y'], printer_json['height_z'])

        sponge_json = environment_json['sponge']
        new_sponge = Sponge(sponge_json['width_x'], sponge_json['depth_y'], sponge_json['height_z'])

        new_environment = Environment(new_printer, new_sponge)

        new_settings = Settings(new_environment)

        return new_settings

    @staticmethod
    def float_to_settings(float_list):

        new_printer = Printer(float_list[0], float_list[1], float_list[2])
        new_sponge = Sponge(float_list[3], float_list[4], float_list[5])

        new_environment = Environment(new_printer, new_sponge)

        new_settings = Settings(new_environment)

        return new_settings

    def settings_to_json(settings):

        json = {
                  "environment" : {
                    "printer" : {
                      "bed_width_x" : settings.environment.printer.bed_width_x,
                      "bed_depth_y" : settings.environment.printer.bed_depth_y,
                      "height_z" : settings.environment.printer.height_z
                    },
                    "sponge" : {
                      "width_x" : settings.environment.sponge.width_x,
                      "depth_y" : settings.environment.sponge.depth_y,
                      "height_z" : settings.environment.sponge.height_z
                    }
                  }
                }

        return json

