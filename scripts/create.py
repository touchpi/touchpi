from string import Template
from os import path, makedirs, chdir
from common import get_home_dir


print('==================================================================================================')
print('Create app scaffolding')
print('--------------------------------------------------------------------------------------------------')
chdir(path.dirname(__file__))
print('Working directory for this script is changed to :' + path.dirname(__file__))
print('Target directory for app scaffolding is :' + get_home_dir() + '/app')
print('--------------------------------------------------------------------------------------------------')


def write_template(filename, content):
    if path.isfile(filename):
        print("File already exists!")
    else:
        makedirs(path.dirname(filename), exist_ok=True)
        f = open(filename, "x")
        f.write(content)
        f.close()


app_name = input("Enter app name (in lower case): ")
app_folder = "../touchpi/app/" + app_name + "/"
templates = [".py", ".toml", ".md"]

for a_template in templates:
    with open("template/template" + a_template) as t:
        template = Template(t.read())
    substituted = template.safe_substitute({'APPNAME': app_name, 'CLASSNAME': app_name.capitalize()})
    if a_template == ".md":
        print("Writing README.md")
        write_template(app_folder + "README.md", substituted)
    else:
        print("Writing " + app_name + a_template)
        write_template(app_folder + app_name + a_template, substituted)

print("Writing __init__.py")
write_template(app_folder + "__init__.py", "")
print("Don't forget to add new files to your source code repository.")
print('==================================================================================================')