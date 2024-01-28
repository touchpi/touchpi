from touchpi.common.config import settings, log, scheduler
from PySimpleGUI import Window, Button


def load_app_settings(appname):
    # Used in App class and OS class initialisation
    log.debug("Load settings of app: " + appname)
    filename = settings["_core_app_pre_path"] + "/" + appname + "/" + appname + ".toml"
    settings.load_file(path=filename)


def app_settings_valid(app):
    # Used in App class and OS class initialisation
    try:
        log.debug("Classname of " + app + ": " + settings[app + "_classname"])
        log.debug("Type of app " + app + ": " + settings[app + "_apptype"])
    except KeyError:
        return False
    else:
        return True


def disable_mouse_over(window: Window):
    # Used in App class und Desktop class initialisation
    # Default mouseover color behavior in pysimplegui hang sometimes at raspberrys and touch devices.
    # Currently only mouseover by buttons are disabled
    if not settings["_core_button_mouseover"]:
        log.info("Disable button mouseover coloring")
        gui_elements = window.element_list()
        for element in gui_elements:
            if type(element) == Button:
                element.Widget.config(activeforeground=element.Widget.cget('fg'),
                                      activebackground=element.Widget.cget('bg'))


def get_value(an_event, a_value):
    # helper function to get an event value. Events values can be inside a list, dict or direct attached to an event
    # used in Ss and in can be used in all apps via the facade method get_event_value in App class.
    if type(a_value) == list:
        ret = a_value[0]
    else:
        try:
            ret = a_value[an_event]
        except KeyError:
            ret = None
    return ret


def start_scheduler():
    # Used in App class und OS class initialisation
    return scheduler.start()


def get_scheduler():
    # Used in App class und OS class initialisation
    return str(scheduler) + " with status: " + str(bool(scheduler.state))


log.success("Init common package in environment: " + settings["_core_environment"])
