from os import scandir, path, getcwd, walk, remove
from pathlib import Path
from zipfile import ZipFile


class Model:
    def __init__(self):
        self.error_text = ''
        self.home_dir = getcwd() + '/touchpi/app/'
        self.download_backup = self.home_dir + '_webconfig/backup.zip'
        self.download_backup_exists = False

    def get_toml_filename(self, app, local=False):
        if local:
            return self.home_dir + app + "/" + app + '.local.toml'
        else:
            return self.home_dir + app + "/" + app + '.toml'

    def get_apps(self):
        try:
            apps = [f.name for f in scandir(self.home_dir) if f.is_dir()]
            for app in apps.copy():
                if not path.isfile(self.get_toml_filename(app)):
                    apps.remove(app)
            if not apps:
                self.error_text = "No apps with config toml found."
            else:
                apps.sort()
                self.error_text = ''
            return apps
        except FileNotFoundError:
            self.error_text = "Wrong  home directory"
            return []

    def get_default_toml(self, app):
        return Path(self.get_toml_filename(app)).read_text()

    def get_local_toml(self, app):
        local_toml = self.get_toml_filename(app, local=True)
        if path.exists(local_toml) and path.getsize(local_toml) > 0:
            local_toml_value = Path(local_toml).read_text()
        else:
            local_toml_value = '[default]\n\n[development]\n\n[production]\n'
        return local_toml_value

    def save_local_toml(self, app, local_toml_value):
        Path(self.get_toml_filename(app, local=True)).write_text(local_toml_value)

    def backup_toml(self):
        if path.exists(self.download_backup):
            remove(self.download_backup)
        file_list = []
        for root, directories, files in walk('./touchpi/app'):
            for filename in files:
                if filename.endswith('.local.toml'):
                    filepath = path.join(root, filename)
                    file_list.append(filepath)
        if file_list:
            with ZipFile(self.download_backup, 'w') as a_zip:
                for file in file_list:
                    a_zip.write(file)
        if path.exists(self.download_backup):
            self.download_backup_exists = True
        else:
            self.download_backup_exists = False
