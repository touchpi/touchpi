from touchpi.appbase.app import App, settings, log
from touchpi.appbase.scheduler import add_onetime_job, next_run_time_in_seconds, remove_job, modify_job
from PySimpleGUI import Sizer, Button
from os import system


class ScreenSaver(App):
    def __init__(self):
        super().__init__()
        self.screensaver = False
        self.job = None
        self.start_timer()
        self.last_app = None

    @staticmethod
    def layout():
        layout = [[Sizer(385, 0)]]
        layout += [[Button(expand_x=True,
                           expand_y=True,
                           size=(1, 16),
                           pad=0,
                           button_color='black',
                           mouseover_colors='black',
                           key="_screensaver_btn_off")]]
        return layout

    def pre_trigger(self):
        self.screensaver = True
        ScreenSaver.set_backlight("off")
        self.window.write_event_value("_core_ev_hide_buttons", None)
        self.stop_timer()

    def post_trigger(self):
        self.screensaver = False
        self.start_timer()
        self.window.write_event_value("_core_ev_show_buttons", None)
        ScreenSaver.set_backlight("on")

    def close_trigger(self):
        log.debug("Screensaver cleanup.")
        ScreenSaver.set_backlight("on")
        self.stop_timer()

    @staticmethod
    def set_backlight(switch: str):
        if settings["_screensaver_switch_backlight"]:
            system("xset dpms force " + switch + " > /dev/null 2>&1")

    def start_timer(self):
        self.job = add_onetime_job(self.run_job,
                                   next_run_time=next_run_time_in_seconds(settings["_screensaver_display_saving_sec"]))
        log.debug("Screensaver timer enabled.")

    def run_job(self):
        self.write_safe_event_value("_screensaver_on_requested_by_timer", None)

    def stop_timer(self):
        remove_job(self.job)
        self.job = None

    def delay_timer(self):
        modify_job(self.job, next_run_time=next_run_time_in_seconds(settings["_screensaver_display_saving_sec"]))
        log.debug("Screensaver timer delayed.")

    def update(self, event, values):
        if event == "_screensaver_btn_off":
            if settings["_screensaver_return_home"]:
                self.window.write_event_value("_core_btn_home", None)
            else:
                log.debug("Screensaver closed request show app" + self.last_app)
                self.window.write_event_value("_core_ev_show_app", self.last_app)
            self.window.write_event_value("_core_ev_hide_button_delay_requested", None)
        elif event == "_screensaver_on_requested_by_timer":
            if not self.screensaver:
                log.debug("Screensaver timer requests button Close")
                self.window.write_event_value("_core_btn_close", None)
        elif event == "_screensaver_delay_requested":
            if not self.screensaver:
                self.delay_timer()
        elif event == "_core_ev_last_shown_app":
            self.last_app = self.get_event_value("_core_ev_last_shown_app", values)


if __name__ == '__main__':
    app = ScreenSaver()
    app.run()
