## system core app
This app is used for update the system or restart the device. 
The system app is optional and can be disabled in the core settings
Update scripts depends different on the environment. 
Production update can be different from development update.
If a development environment is set, a Quit and "Power off" button is available too.
Development environment is set via environment variable ENV_FOR_DYNACONF=development
To make change persistent, add e.g. in .bashrec export ENV_FOR_DYNACONF=development 