## core app
The core app is used for global settings and hiding core buttons.
It reserves the app namespace _core for desktop gui elements, events and settings and base app settings and OS settings.
Hiding of the core buttons is implemented in this app, because app scheduling is needed.   

Settings of the base app and the touchpi OS are set in the _core.toml file in the folder of the app "_core".
To change settings copy the _core.toml file to a _core.local.toml file. Change the settings in this file. 
You can delete the settings which are not changed.
Touchpi is using the settings of the local toml file first. 
Settings which are not in the local toml file but in the original toml file are loaded too.
Settings in the toml files which are not local are under source code control and can change during development.

Certain apps are OS apps and are loaded before the regular apps.
- OS apps are ["_backlight", "_core", "_empty", "_pulse", "_screensaver", "_splash", "_system"]
- foreground OS apps are ["_empty", "_screensaver", "_splash", "_system"]
- background OS apps are ["backlight", "pulse"]

Certain OS apps can be disabled:
- _screensaver app can be disabled with _core_screensaver_app = false
- _system app can be disabled with _core_system_app = false 
- _pulse app can be disabled with _core_pulse_app = false
- _splash app can be disabled with _core_splash_app = false
- _core is initialised as background app when _core_hide_buttons = true (default)

if core_screensaver = True, then _backlight app is loaded too.
The _system app is optional. But it is recommended to load it. It will be loaded as last foreground app.
The _pulse app is optional. 
_splash app is nly shown once when touchpi OS is started (in development)

To log all gui events turn on setting _core_eventlog = true

When no apps could be loaded, then _empty and _system app are loaded as minimal version 
(therefor _empty and _system layout is always loaded ind advance).
