from touchpi.appbase.app import App, settings, log
from PySimpleGUI import VPush, Push, Text, HorizontalSeparator, Multiline, Button


class Message(App):
    def __init__(self):
        super().__init__()
        self.last_app = ""

    @staticmethod
    def layout():
        layout = [[VPush()]]
        layout += [[Push(), Text('Message header', font='Any 15 bold', key='_message-text1'), Push()]]
        layout += [[HorizontalSeparator(pad=5)]]
        layout += [[Push(), Multiline('Message body', key='_message-text2', no_scrollbar=True, font='Any 12',
                    justification="center", size=(settings["_message_wide"], settings["_message_height"]),
                    disabled=True), Push()]]
        layout += [[HorizontalSeparator(pad=5)]]
        layout += [[Push(), Button('Ok', key="_message_btn-ok", border_width=1), Push()]]
        layout += [[VPush()]]
        return layout

    def pre_trigger(self):
        self.window.write_event_value("_core_ev_hide_buttons", None)

    def post_trigger(self):
        self.window.write_event_value("_core_ev_show_buttons", None)

    def update(self, event, values):
        if event == "_message_ev":
            message_values = self.get_event_value("_message_ev", values)
            self.window['_message-text1'].update(message_values[0])
            self.window['_message-text2'].update(message_values[1])
            log.debug("Message text set: " + message_values[1])
            self.window.write_event_value("_core_ev_show_app", "_message")
        elif event == "_message_btn-ok":
            log.debug("Message Ok. Switching back to last app: " + self.last_app)
            self.window.write_event_value("_core_ev_show_app", self.last_app)
        elif event == "_core_ev_last_shown_app":
            self.last_app = self.get_event_value("_core_ev_last_shown_app", values)


if __name__ == '__main__':
    app = Message()
    app.run()
