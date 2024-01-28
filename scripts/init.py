#!/usr/bin/env python3
from string import Template
from os import path, makedirs, chdir


chdir(path.dirname(__file__))


def write_template(filename, content):
    if path.isfile(filename):
        print("File already exists!")
    else:
        makedirs(path.dirname(filename), exist_ok=True)
        f = open(filename, "x")
        f.write(content)
        f.close()


appname = input("Enter app name (in lower case): ")
appfolder = "../touchpi/app/" + appname + "/"
templates = [".py", ".toml", ".md"]

for a_template in templates:
    with open("template/template" + a_template) as t:
        template = Template(t.read())
    substituted = template.safe_substitute({'APPNAME': appname, 'CLASSNAME': appname.capitalize()})
    if a_template == ".md":
        print("Writing README.md")
        write_template(appfolder + "README.md", substituted)
    else:
        print("Writing " + appname + a_template)
        write_template(appfolder + appname + a_template, substituted)

print("Writing __init__.py")
write_template(appfolder + "__init__.py", "")
print("Don't forget to add files to your source code repository.")
