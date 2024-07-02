from nicegui import ui, events, app as server
from touchpi.app._webconfig.model import Model


class View:
    def __init__(self):
        self.current_app = ''
        self.data = Model()

        text = "To change a config, copy the line of the Default-Toml "
        text += "to Local-Toml, change the value of the config and save it."
        with ui.row().classes('w-full') as self.top_button_row:
            self.config_button = ui.dropdown_button('configure', icon='upload', auto_close=True)
            ui.button('backup', icon='download', on_click=lambda: self.backup_toml())
        with ui.card().classes('w-full') as self.container:
            with ui.row().classes('w-full justify-center'):
                self.text = ui.label(text)
            ui.space()
            with ui.splitter().classes('w-full h-full') as splitter:
                with splitter.before:
                    ui.label('Default-Toml:').style('font-weight: bold')
                    self.code = ui.code('')
                with splitter.after:
                    ui.label('Local-Toml:').style('font-weight: bold')
                    self.editor = ui.codemirror('', language='TOML', on_change=lambda: self.config_changed())
                    self.editor.classes('h-full')
                    ui.space()
                    with ui.row().classes('w-full justify-center'):
                        self.save_button = ui.button('Save', on_click=lambda: self.save_config())
                        self.cancel_button = ui.button('Cancel', on_click=lambda: self.cancel_config())

        self.container.set_visibility(False)
        self.create_dropdown_button_elements()

    def create_dropdown_button_elements(self):
        self.config_button.clear()
        apps = self.data.get_apps()
        if not self.data.error_text:
            with self.config_button:
                with ui.column():
                    for app in apps:
                        if app == '_core':
                            ui.chip(app, on_click=self.get_chip_event, color='dark-grey').props('outline square')
                        elif app.startswith('_'):
                            ui.chip(app, on_click=self.get_chip_event, color='grey').props('outline square')
                        else:
                            ui.chip(app, on_click=self.get_chip_event).props('outline square')
        else:
            ui.notify(self.data.error_text)
        with self.config_button:
            ui.button('REFRESH LIST', icon='autorenew', on_click=lambda: self.create_dropdown_button_elements())
        ui.notify('App list loaded')

    def get_chip_event(self, event: events.ValueChangeEventArguments):
        self.load_config(event.sender._text)

    def load_config(self, app):
        self.code.content = self.data.get_default_toml(app)
        self.editor.value = self.data.get_local_toml(app)
        # self.config_button.set_visibility(False)
        self.top_button_row.set_visibility(False)
        self.container.set_visibility(True)
        self.save_button.set_visibility(False)
        self.current_app = app
        ui.notify('Config of ' + app + ' loaded.')

    def config_changed(self):
        self.save_button.set_visibility(True)

    def save_config(self):
        self.save_button.set_visibility(False)
        self.data.save_local_toml(self.current_app, self.editor.value)
        ui.notify('Config of ' + self.current_app + ' saved.')

    def cancel_config(self):
        self.container.set_visibility(False)
        # self.config_button.set_visibility(True)
        self.top_button_row.set_visibility(True)
        ui.notify('Config of ' + self.current_app + ' canceled.')
        self.current_app = ''
        self.editor.value = ''

    def backup_toml(self):
        self.data.backup_toml()
        if self.data.download_backup_exists:
            ui.download(self.data.download_backup)
            ui.notify('All local toml files downloaded as zip.')
        else:
            ui.notify('There are no local toml files.')

    @classmethod
    def stop(cls):
        server.shutdown()

    @classmethod
    def run(cls, host, port):
        ui.run(title='touchpi-config', favicon='https://touchpi.bruu.eu/img/favicon.png', host=host, port=port,
               show=False, reload=False)
