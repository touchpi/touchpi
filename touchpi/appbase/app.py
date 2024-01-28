import touchpi.common.window
from touchpi.common import settings, log, load_app_settings, app_settings_valid, start_scheduler, get_scheduler, \
                     disable_mouse_over, get_value
from PySimpleGUI import Window, WINDOW_CLOSE_ATTEMPTED_EVENT
from os import path
from inspect import stack


class App:
    def __init__(self):
        self.window = None
        app_name = App.get_app_name(2)
        if touchpi.common.window.os_window is None:  # App is starting locally, when os_windows does not exist
            load_app_settings(app_name)  # OS is loading the app settings in advance and checks them.
            if not app_settings_valid(app_name):
                raise KeyError  # When app settings are loaded locally with error, then quit with an exception
            self.window = self.app_window(self.layout(), settings[app_name + "_apptype"] + " " + app_name)
            log.info("App " + app_name + " initialised with a local window." + str(self.window))
            start_scheduler()
            log.info("App " + app_name + " initialised with a local scheduler " + get_scheduler())
            disable_mouse_over(self.window)
        else:
            self.window = touchpi.common.window.os_window

    @staticmethod
    def get_app_name(caller_hierarchy=1):
        # Static method provided for apps (caller_hierarchy=1 (default)
        # Static method used in base App (caller_hierarchy=2)
        # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
        # tuple-like operations may be deprecated and removed in the future
        file_of_caller = stack()[caller_hierarchy][1]
        app = path.splitext(path.basename(file_of_caller))[0]
        return app

    @staticmethod
    def get_app_folder():
        # Static method provided for apps. Usually in loading resources (e.g. images) in the static layout method.
        file_of_caller = stack()[1][1]
        app = path.splitext(path.basename(file_of_caller))[0]
        folder = settings["_core_app_pre_path"] + "/" + app + "/"
        return folder

    @staticmethod
    def get_app_width():
        # Static method provided for apps. Usually in building the static layout.
        return settings["_core_window_size_x"] - 94

    @staticmethod
    def get_app_height():
        # Static method provided for apps. Usually in building the static layout.
        return settings["_core_window_size_y"] - 98

    @staticmethod
    def layout():
        # Static method für building the static layout. Will be overwritten in frontend apps.
        return [[]]

    @staticmethod
    def app_window(layout, title):
        # Just called in local app
        window = Window(title,
                        layout,
                        font=settings["_core_default_font"],
                        location=(settings["_core_window_location_x"], settings["_core_window_location_y"]),
                        size=(App.get_app_width(), App.get_app_height() + 14),
                        enable_close_attempted_event=True,
                        margins=(0, 0),
                        finalize=True)
        window.bind("<Escape>", "Quit")
        log.debug("Local Window initialised.")
        return window

    @classmethod
    def get_event_value(cls, an_event, a_value):
        # helper function to get easy an event value.
        # Events values can be inside a list, dict or direct attached to an event
        return get_value(an_event, a_value)

    def write_safe_event_value(self, an_event, a_value):
        # helper function for writing safe events in scheduled jobs (threaded code)
        try:
            self.window.write_event_value(an_event, a_value)
        except AttributeError:
            return False
        else:
            return True

    def message(self, header: str, body: str):
        self.write_safe_event_value("_message_ev", (header, body))

    def pre_trigger(self):
        # Method called before app gets visible in desktop. Can be overwritten in the app.
        pass

    def post_trigger(self):
        # Method called after app gets hidden in desktop. Can be overwritten in the app.
        pass

    def close_trigger(self):
        # Method called when system ends in dk. Can be overwritten in the app.
        pass

    def update(self, event, values):
        # Event loop. Can be overwritten in the app.
        pass

    def run(self):
        # run is used in a local app
        log.success('Starting eventloop.')
        while True:
            event, values = self.window.read()
            if settings["_core_eventlog"]:
                log.debug("Event: " + str(event) + ";  Values:" + str(values))
            if event in (WINDOW_CLOSE_ATTEMPTED_EVENT, 'Quit'):
                log.debug('App window close attempt.')
                break
            self.update(event, values)
        self.close_trigger()
        self.window.close()
        log.debug('App closing')
