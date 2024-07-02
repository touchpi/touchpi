from touchpi.appbase.app import App, settings, log
from touchpi.appbase.scheduler import add_onetime_job_now
from touchpi.app._webconfig.view import View


class Webconfig(App):
    def __init__(self):
        super().__init__()
        self.job = None
        self.webview = View()
        self.start_server()

    def start_server(self):
        self.job = add_onetime_job_now(self.run_job)
        log.info("Starting webserver at: " + settings["_webconfig_host"] + ":" + str(settings["_webconfig_port"])
                 + " with job id: "+ str(self.job))

    def run_job(self):
        self.webview.run(settings["_webconfig_host"], settings["_webconfig_port"])

    def close_trigger(self):
        log.info("Stopping webserver." )
        self.webview.stop()
        self.job = None


if __name__ == '__main__':
    app = Webconfig()
    app.run()
