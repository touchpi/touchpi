from touchpi.common import log, settings, disable_mouse_over, get_value
from PySimpleGUI import Window, Column, Button, pin, WINDOW_CLOSE_ATTEMPTED_EVENT


class Desktop:
    def __init__(self, layout: list):
        self.success = True
        self.current_app = None
        self.first_app = None
        self.last_app = None
        self.foreground_apps = []
        self.window = self.os_window(layout)
        disable_mouse_over(self.window)
        if not settings["_core_screensaver_app"]:
            self.window['_core_btn_close'].update(disabled=True)
        self.show_core_buttons()
        log.success("Touchpi Desktop Initialisation finished.")

    def os_window(self, layout):
        try:
            win = Window('Desktop',
                         self.desktop_layout(layout),
                         font=settings["_core_default_font"],
                         location=(settings["_core_window_location_x"], settings["_core_window_location_y"]),
                         size=(settings["_core_window_size_x"], settings["_core_window_size_y"]),
                         enable_close_attempted_event=True,
                         no_titlebar=True,
                         margins=(0, 0),
                         finalize=True)
        except Exception:
            self.success = False
            win = Window('BlueScreen',
                         [[]],
                         location=(settings["_core_window_location_x"], settings["_core_window_location_y"]),
                         size=(settings["_core_window_size_x"], settings["_core_window_size_y"]),
                         enable_close_attempted_event=True,
                         no_titlebar=True,
                         margins=(0, 0),
                         finalize=True)
            log.error("Error in an app Layout. Please check every frontend app with a standalone app call.")
            win.write_event_value("Quit", 12)
        else:
            log.info("Touchpi OS Window initialised.")
        return win

    @staticmethod
    def xbutton(name: str, label: str):
        button = [[Button(label,
                          font='any 15',
                          pad=(0, 0),
                          expand_x=True,
                          key="_core_btn_" + name)]]
        layout = pin(Column(button,
                            pad=(0, 0),
                            expand_x=True,
                            key="_core_col_" + name), expand_x=True)

        return layout

    @staticmethod
    def ybutton(name: str, label: str):
        button = [[Button(label,
                          font='any 15',
                          pad=(0, 0),
                          expand_y=True,
                          key="_core_btn_" + name)]]
        layout = pin(Column(button,
                            pad=(0, 0),
                            expand_y=True,
                            key="_core_col_" + name), expand_y=True)

        return layout

    @staticmethod
    def sizer(name: str, size: int, vis: bool):
        layout = pin(Column([[]],
                            size=(size, 0),
                            pad=(0, 0),
                            visible=vis,
                            key="_core_col_" + name))
        return layout

    @staticmethod
    def desktop_layout(apps_layout):
        layout = [[Desktop.xbutton("home", "Home")]]

        row = [Desktop.ybutton("left", "<")]

        inner_space = [[Desktop.sizer("sizer_left", 45, False),
                        Desktop.sizer("sizer_middle", settings["_core_window_size_x"] - 90, True),
                        Desktop.sizer("sizer_right", 45, False)]]
        inner_space += apps_layout

        row.append(Column(inner_space, pad=(0, 0), expand_x=True, expand_y=True))
        row.append(Desktop.ybutton("right", ">"))

        layout += [[row]]
        layout += [[Desktop.xbutton("close", "Close")]]

        log.info("Touchpi Desktop Layout initialised.")
        return layout

    def set_foreground_apps(self, foreground_apps: list):
        # Foreground app data is initialised after Desktop initialisation (windows/layout setup) with this method
        log.debug(foreground_apps)
        if foreground_apps:
            self.first_app = foreground_apps[0]
            self.current_app = self.first_app
            self.last_app = foreground_apps[-1]
            self.foreground_apps = foreground_apps
        else:
            log.error("Desktop got an empty foreground apps dict.")
            self.window.write_event_value("Quit", 12)

    def previous_app(self):
        if self.current_app == self.first_app:
            return None
        else:
            return self.foreground_apps[self.foreground_apps.index(self.current_app) - 1]

    def next_app(self):
        if self.current_app == self.last_app:
            return None
        else:
            return self.foreground_apps[self.foreground_apps.index(self.current_app) + 1]

    def show_app(self, appname):
        if appname is not None:
            self.window["_core_col_" + self.current_app].update(visible=False)
            self.window.write_event_value("_core_ev_post_trigger", self.current_app)
        if appname != self.current_app:
            if appname is None:
                appname = self.current_app
            if appname == self.first_app:
                self.window['_core_btn_left'].update(disabled=True)
                self.window['_core_btn_home'].update(disabled=True)
            else:
                self.window['_core_btn_left'].update(disabled=False)
                self.window['_core_btn_home'].update(disabled=False)
            if appname == self.last_app:
                self.window["_core_btn_right"].update(disabled=True)
            else:
                self.window["_core_btn_right"].update(disabled=False)
            self.window.write_event_value("_core_ev_last_shown_app", self.current_app)
            self.window["_core_col_" + appname].update(visible=True)
            self.window.write_event_value("_core_ev_pre_trigger", appname)
            self.current_app = appname

    def show_core_buttons(self):
        if settings["_core_hide_home_button"]:
            self.window["_core_col_home"].update(visible=False)
        else:
            self.window["_core_col_home"].update(visible=True)
        if settings["_core_hide_close_button"]:
            self.window["_core_col_close"].update(visible=False)
        else:
            self.window["_core_col_close"].update(visible=True)
        if settings["_core_hide_navigation_buttons"]:
            self.window["_core_col_right"].update(visible=False)
            self.window["_core_col_left"].update(visible=False)
            self.window["_core_col_sizer_left"].update(visible=True)
            self.window["_core_col_sizer_right"].update(visible=True)
        else:
            self.window["_core_col_right"].update(visible=True)
            self.window["_core_col_left"].update(visible=True)
            self.window["_core_col_sizer_left"].update(visible=False)
            self.window["_core_col_sizer_right"].update(visible=False)

    def hide_core_buttons(self):
        self.window['_core_col_home'].update(visible=False)
        self.window['_core_col_close'].update(visible=False)
        self.window['_core_col_right'].update(visible=False)
        self.window['_core_col_left'].update(visible=False)
        self.window["_core_col_sizer_left"].update(visible=True)
        self.window["_core_col_sizer_right"].update(visible=True)

    def update(self, event, values):
        if event == WINDOW_CLOSE_ATTEMPTED_EVENT:
            log.info("Desktop window close attempt.")
            self.window.write_event_value("Quit", None)
        elif event == "_core_ev_start_desktop":
            log.debug('Start desktop event received.')
            self.window.write_event_value("_core_ev_show_app", None)
        elif event == "_core_btn_home":
            log.debug('Button Home pressed.')
            self.window.write_event_value("_core_ev_show_app", self.first_app)
        elif event == "_core_btn_right":
            log.debug('Button right pressed.')
            next_app = self.next_app()
            if next_app:
                self.window.write_event_value("_core_ev_show_app", next_app)
        elif event == "_core_btn_left":
            log.debug('Button left pressed.')
            previous_app = self.previous_app()
            if previous_app:
                self.window.write_event_value("_core_ev_show_app", previous_app)
        elif event == "_core_btn_close":
            if self.current_app != "_screensaver":
                log.debug('Button Close pressed.')
                self.window.write_event_value("_core_ev_show_app", "_screensaver")
        elif event == "_core_ev_show_app":
            self.show_app(get_value("_core_ev_show_app", values))
        elif event == "_core_ev_show_buttons":
            self.show_core_buttons()
        elif event == "_core_ev_hide_buttons":
            self.hide_core_buttons()
        elif event == "_core_mouse_btn_1":
            if self.current_app != "_screensaver":
                self.window.write_event_value("_screensaver_delay_requested", None)
                if self.current_app != "_message":
                    self.show_core_buttons()
                    self.window.write_event_value("_core_ev_hide_button_delay_requested", None)
