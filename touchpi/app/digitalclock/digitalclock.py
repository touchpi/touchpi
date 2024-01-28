from touchpi.appbase.app import App
from PySimpleGUI import VPush, Push, Text
from datetime import datetime


class DigitalClock(App):
    def __init__(self):
        super().__init__()

    @staticmethod
    def layout():
        layout = [[VPush()]]
        layout += [[Push(), Text('Day loading', font='Any 18', key='digitalclock_day'), Push()]]
        layout += [[Push(), Text('Date loading', font='Any 18', key='digitalclock_date'), Push()]]
        layout += [[Push(), Text('Time loading', font='Any 36', key='digitalclock_time'), Push()]]
        layout += [[VPush()]]
        return layout

    def update(self, event, values):
        if event == "_pulse_1":
            data = datetime.now()
            self.window['digitalclock_day'].update(data.strftime("%A"))
            self.window['digitalclock_date'].update(data.strftime("%d.%m.%Y"))
            self.window['digitalclock_time'].update(data.strftime("%H:%M:%S"))


if __name__ == '__main__':
    app = DigitalClock()
    app.window.write_event_value("_pulse_1", None)
    app.run()
