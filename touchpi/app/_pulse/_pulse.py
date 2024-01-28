from touchpi.appbase.app import App, settings, log
from touchpi.appbase.scheduler import add_onetime_job_now
from time import sleep


class Pulse(App):
    def __init__(self):
        super().__init__()

        self.job = None
        self.pulse_list = settings["_pulse_factors"]
        self.pulse = settings["_pulse_in_second"]
        assert self.pulse_list, "The setting pulse_factors is empty"
        assert (self.check_pulse_list()), "A setting in pulse_factors is not a multiple of pulse_in_second."
        self.do_long_operation()

    def check_pulse_list(self):
        for p in self.pulse_list:
            if p % self.pulse != 0:
                return False
        return True

    def do_long_operation(self):
        pulse_list = []
        for f in self.pulse_list:
            pulse_list.append(f * self.pulse)
        self.job = add_onetime_job_now(self.run_job, args=[self.pulse, pulse_list])
        log.debug("Endless pulse job started: " + str(self.job))

    def run_job(self, pulse, pulse_list: list):
        running = True
        elapsed_time = 0
        max_time = pulse_list[-1]
        while running:
            sleep(pulse)
            elapsed_time = elapsed_time + pulse
            for t in pulse_list:
                if elapsed_time % t == 0:
                    running = self.write_safe_event_value("_pulse_" + str(t), None)
            if elapsed_time >= max_time:
                log.debug("Reset elapsed_time at: " + str(elapsed_time))
                elapsed_time = 0


if __name__ == '__main__':
    app = Pulse()
    app.run()
