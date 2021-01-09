
from PyQt5.QtWidgets import QMenuBar, QAction
from gcode_viewer.gui.menu_bar.change_environment_window import Change_Environment_Window
from gcode_viewer.util.file_handler import File_Handler


class Menu_Bar(QMenuBar):

    def __init__(self, settings):
        super().__init__()

        self.initUI()
        self.observer = None

        self.settings = settings

    def initUI(self):
        self.file_handler = File_Handler()

        settings_menu = self.addMenu("Settings")

        change_settings_action = QAction("Change the Settings", self)
        settings_menu.addAction(change_settings_action)

        change_settings_action.triggered.connect(self.change_settings_action)

    def change_settings_action(self):

        changed_settings = Change_Environment_Window().change_environment(settings=self.settings)
        self.notify_observer("new_settings", changed_settings)

    def notify_observer(self, type, par1, par2 = None):

        self.observer.update(type, par1, par2)
