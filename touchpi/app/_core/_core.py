from touchpi.appbase.app import App, log, settings
from touchpi.appbase.scheduler import add_onetime_job, next_run_time_in_seconds, remove_job, modify_job


class Core(App):
    def __init__(self):
        super().__init__()
        self.job = None

    def start_timer(self):
        self.job = add_onetime_job(self.run_job,
                                   next_run_time=next_run_time_in_seconds(settings["_core_hide_buttons_sec"]))
        log.debug("Hide desktop button timer enabled.")

    def run_job(self):
        self.write_safe_event_value("_core_ev_hide_buttons", None)
        self.job = None

    def delay_timer(self):
        modify_job(self.job, next_run_time=next_run_time_in_seconds(settings["_core_hide_buttons_sec"]))
        log.debug("Hide desktop button timer delayed.")

    def stop_timer(self):
        remove_job(self.job)
        self.job = None

    def close_trigger(self):
        log.debug("Hide Button cleanup.")
        self.stop_timer()

    def update(self, event, values):
        if event == "_core_ev_hide_button_delay_requested":
            if self.job:
                self.delay_timer()
            else:
                self.start_timer()


if __name__ == '__main__':
    app = Core()
    app.run()
