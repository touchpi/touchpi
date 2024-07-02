import touchpi.common.window
from touchpi.common import log, settings
from touchpi.common import start_scheduler, get_scheduler, load_app_settings, app_settings_valid, get_value
from .desktop import Desktop
from PySimpleGUI import theme, Column
import pydoc


class OS:
    def __init__(self):
        log.info("Touchpi OS is starting...")
        self.apps_to_load = settings["_core_apps"]
        log.info("Touchpi Version: " + settings["_core_os_version"])
        self.all_apps = {}
        self.load_core_apps_settings(["_screensaver", "_system", "_pulse", "_message", "_webconfig"])
        self.load_apps_settings()
        theme_name = theme(settings["_core_color_theme"])
        log.info("Color theme is " + theme_name)
        layout = self.load_apps_layouts(self.load_core_apps_layouts(["_screensaver", "_system", "_message"]))
        self.desktop = Desktop(layout)
        if self.desktop.success:
            touchpi.common.window.os_window = self.desktop.window
            start_scheduler()
            log.info("Touch OS Scheduler " + get_scheduler())
            core_apps = self.initialise_core_apps()
            self.all_apps = self.initialise_apps()
            self.all_apps.update(core_apps)  # append core_apps dict into all_apps dict
            self.desktop.set_foreground_apps(self.get_foreground_apps())
            log.success("Touchpi OS Initialisation finished.")

    @staticmethod
    def default_column(name: str, lay, vis: bool):
        layout = Column(lay,
                        expand_x=True,
                        expand_y=True,
                        pad=(0, 0),
                        visible=vis,
                        key="_core_col_" + name)
        return layout

    @classmethod
    def load_core_apps_settings(cls, core_settings_apps: list):
        log.debug("Loading core app settings for: " + str(core_settings_apps))
        for app in core_settings_apps:
            load_app_settings(app)
            if not app_settings_valid(app):
                raise KeyError
        log.info("Settings for core apps loaded.")

    @classmethod
    def load_core_apps_layouts(cls, core_foreground_apps: list):
        log.debug("Loading core apps layouts for: " + str(core_foreground_apps))
        col_row = []
        for app in core_foreground_apps:
            app_module = pydoc.locate("touchpi.app." + app + "." + app)
            app_layout = getattr(app_module, settings[app + "_classname"])
            # col_row.append(Column(app_layout.layout(), visible=False, key="__core_column-" + app))
            col_row.append(OS.default_column(app, app_layout.layout(), False))
        log.info("Core app layouts loaded.")
        return col_row

    @classmethod
    def initialise_core_apps(cls):
        core_apps = {}
        core_apps_to_load = ["_message", "_system"]
        if settings["_core_screensaver_app"]:
            core_apps_to_load.extend(["_screensaver"])
        if settings["_core_pulse_app"]:
            core_apps_to_load.append("_pulse")
        if settings["_core_webconfig_app"]:
            core_apps_to_load.append("_webconfig")
        #  There is logic in _core app for auto hiding desktop buttons
        if settings["_core_hide_buttons"]:
            core_apps_to_load.append("_core")
        log.debug("Initialise core apps: " + str(core_apps_to_load))
        for app in core_apps_to_load:
            app_module = pydoc.locate("touchpi.app." + app + "." + app)
            app_class = getattr(app_module, settings[app + "_classname"])
            instance = app_class()
            core_apps[app] = instance
        log.info("Core apps Initialised." + str(core_apps))
        return core_apps

    def load_apps_settings(self):
        log.debug("Loading app settings.")
        app_list = self.apps_to_load.copy()
        for app in app_list:
            load_app_settings(app)
            if not app_settings_valid(app):
                log.warning("Wrong app type of app " + app + ". App not loaded.")
                #  Delete all occurrences of this app in input list
                self.apps_to_load = [value for value in self.apps_to_load if value != app]
        log.debug("Apps settings to be loaded: " + str(app_list))
        log.debug("Apps settings loaded: " + str(self.apps_to_load))
        log.info("App settings loaded.")

    def load_apps_layouts(self, core_layout):
        log.debug("Loading app layouts.")
        col_row = core_layout
        app_list = self.apps_to_load.copy()
        for app in app_list:
            if settings[app + "_apptype"] == "foreground":
                try:
                    app_module = pydoc.locate("touchpi.app." + app + "." + app)
                    app_layout = getattr(app_module, settings[app + "_classname"])
                except (KeyError, AttributeError):
                    log.warning("Could not load layout of " + str(app) + ". App not loaded.")
                    #  Delete all occurrences of this app in input list
                    self.apps_to_load = [value for value in self.apps_to_load if value != app]
                else:
                    # col_row.append(Column(app_layout.layout(), visible=False, key="__core_column-" + app))
                    col_row.append(OS.default_column(app, app_layout.layout(), False))
        log.debug("App layouts loaded: " + str(self.apps_to_load))
        log.info("App layouts combined into one layout.")
        return [col_row]

    def initialise_apps(self):
        log.debug("Initialising apps.")
        all_apps = {}
        app_list = self.apps_to_load.copy()
        for app in app_list:
            try:
                app_module = pydoc.locate("touchpi.app." + app + "." + app)
                app_class = getattr(app_module, settings[app + "_classname"])
                instance = app_class()
            except Exception as err:
                log.warning("App " + app + " not loaded. Error: " + str(err) + " " + str(type(err)))
                #  Delete all occurrences of this app in input list
                self.apps_to_load = [value for value in self.apps_to_load if value != app]
            else:
                log.info("App loaded: " + str(instance))
                all_apps[app] = instance
        log.debug("Apps to be loaded: " + str(app_list))
        log.debug("Apps loaded: " + str(self.apps_to_load))
        log.debug("Apps objects: " + str(all_apps))
        log.info("App loading and initialisation finished.")
        return all_apps

    def get_foreground_apps(self):
        foreground_apps = []
        #  Don't declare _screensaver and _message app as foreground app.
        #  _system app is added as last app when settings _core_system_app=true or no app is loaded
        for app in list(self.all_apps.keys()):
            app_type = settings[app + "_apptype"]
            if (app_type == "foreground") and (app not in ["_screensaver", "_message", "_system"]):
                foreground_apps.append(app)
        if settings["_core_system_app"] or len(foreground_apps) == 0:
            foreground_apps.append("_system")
        log.debug("Apps loaded: " + str(list(self.all_apps.keys())))
        log.debug("Foreground navigation apps: " + str(foreground_apps))
        return foreground_apps

    def run(self):
        self.desktop.window.bind("<Escape>", "Quit")
        self.desktop.window.bind('<Button-1>', '_core_mouse_btn_1')
        self.desktop.window.write_event_value("_core_ev_start_desktop", None)
        self.desktop.window.write_event_value("_core_ev_hide_button_delay_requested", None)
        if self.desktop.foreground_apps == ["_system"]:
            log.warning("No user apps loaded.")
            self.desktop.window.write_event_value("_message_ev",
                                                  ("OS Warning",
                                                   "No apps loaded. Check the log and the setting \"_core_apps\""))
        log.success('Starting eventloop.')
        while True:
            event, values = self.desktop.window.read()
            if settings["_core_eventlog"]:
                log.debug("Event: " + str(event) + ";  Values:" + str(values))
            self.desktop.update(event, values)
            if event == 'Quit':
                log.info('Touch OS closing.')
                rc = get_value('Quit', values)
                if rc is None:
                    rc = 0
                break
            elif event == "_core_ev_post_trigger":
                self.all_apps[get_value("_core_ev_post_trigger", values)].post_trigger()
            elif event == "_core_ev_pre_trigger":
                self.all_apps[get_value("_core_ev_pre_trigger", values)].pre_trigger()
            for app in self.all_apps.values():
                try:
                    app.update(event, values)
                except Exception as err:
                    log.warning("Update error in App " + str(app) + " Error: " + str(err) + " " + str(type(err)))
        for app in self.all_apps.values():
            app.close_trigger()
        self.desktop.window.close()
        return rc
