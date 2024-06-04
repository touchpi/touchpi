from touchpi.appbase.app import App, log
from touchpi.appbase.scheduler import add_onetime_job_now
from PySimpleGUI import VPush, Push, Canvas
from touchpi.app.mvg.mvg_data_lib import get_rawdata, convert_rawdata
from touchpi.app.mvg.mvg_draw_lib import MvgDraw


class Mvg(App):
    def __init__(self):
        super().__init__()
        self.app_is_visible = False
        self.job = None
        self.departures = [[], []]
        self.mvg_draw = MvgDraw(self.window['mvg_canvas'].tk_canvas)

    @staticmethod
    def layout():
        layout = [[VPush()]]
        canvas = Canvas(size=(App.get_app_width(), App.get_app_height()), pad=(0, 0), key='mvg_canvas')
        layout += [[Push(), canvas, Push()]]
        layout += [[VPush()]]
        return layout

    def pre_trigger(self):
        self.app_is_visible = True
        self.mvg_draw.init_screen()
        self.do_long_operation()

    def post_trigger(self):
        self.app_is_visible = False

    def do_long_operation(self):
        self.job = add_onetime_job_now(self.run_job)
        log.info("MVG data requested with job id: " + str(self.job))

    def run_job(self):
        try:
            departure_raw_data = get_rawdata()
            self.departures = convert_rawdata(departure_raw_data)
        except ValueError as err:
            log.error("Error in loading data: " + str(err) + " " + str(type(err)))
            self.write_safe_event_value("mvg_load_error", None)
        else:
            self.write_safe_event_value("mvg_updated", None)

    def update(self, event, values):
        if event == '_pulse_60':
            if self.app_is_visible:
                self.do_long_operation()
        elif event == 'mvg_updated':
            self.job = None
            self.mvg_draw.draw(self.departures)
        elif event == 'mvg_load_error':
            self.job = None
            log.debug("Drawing error load screen ")
            self.mvg_draw.init_screen("Error loading data.", 'red')


if __name__ == '__main__':
    app = Mvg()
    app.pre_trigger()
    app.run()
