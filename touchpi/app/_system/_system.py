from touchpi.appbase.app import App, log, settings
from PySimpleGUI import VPush, Push, Button, HorizontalSeparator
from os import system


class System(App):
    def __init__(self):
        super().__init__()

    @staticmethod
    def layout():
        layout = [[VPush()]]
        layout += [[Push(), Button('Update', key='_system_btn_update'), Push()]]
        if settings["_core_environment"] == 'development':
            layout += [[HorizontalSeparator(pad=15)]]
            layout += [[Push(), Button('Quit', key='_system_btn_quit', button_color="red"), Push()]]
        layout += [[HorizontalSeparator(pad=15)]]
        layout += [[Push(), Button('Restart', key='_system_btn_restart'), Push()]]
        layout += [[HorizontalSeparator(pad=15)]]
        layout += [[Push(), Button('Reboot', key='_system_btn_reboot'), Push()]]
        if settings["_core_environment"] == 'development':
            layout += [[HorizontalSeparator(pad=15)]]
            layout += [[Push(), Button('Power Off', key='_system_btn_poweroff', button_color="red"), Push()]]
        layout += [[VPush()]]
        return layout

    def update(self, event, values):
        if event in '_system_btn_poweroff':
            log.info("System shutdown requested.")
            system('sudo poweroff')
        elif event in '_system_btn_update':
            log.info("System update requested.")
            self.window.write_event_value("Quit", 10)
        elif event in '_system_btn_restart':
            log.info("System restart requested.")
            self.window.write_event_value("Quit", 11)
        elif event in '_system_btn_reboot':
            log.info("System reboot requested.")
            system('sudo reboot')
        elif event in '_system_btn_quit':
            log.info("System quit requested.")
            self.window.write_event_value("Quit", 0)


if __name__ == '__main__':
    app = System()
    app.run()
