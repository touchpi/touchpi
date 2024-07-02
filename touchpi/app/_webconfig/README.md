## _webconfig app
This background app starts a FastAPI job (with Starlette and Uvicorn) server which is packaged in the NiceGUI package.
With this app you can configure now all touchpi toml config files with a browser.
Call the URL http://<your raspi ip >:port (default port is 8080) in your browser
To use this feature, you have to switch on the app with the _core configuration _core_webconfig_app = true 
You can change the server port in the _webconfig.local.toml file.

Note:
Currently, there is no authentication and encryption.
When the app is switched on, everybody in your LAN can change your touchpi configuration.
If you want to avoid this, you can install an additional reverse proxy (Appache, NGINX, TRAEFIK etc. ) on your pi.
