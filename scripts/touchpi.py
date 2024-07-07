#!/usr/bin/env python3
from sys import argv
from common import get_home_dir, call_python_script


help_text = """====================================================================
Your touchpi script starter:
-------------------------------------------------------------------- 
Start this script like
    python3 touchpi.py USAGE     or
    ./touchpi.py USAGE           or
    touchpi USAGE                (after setup)

Usage:
touchpi start
touchpi update
touchpi setup
touchpi create
touchpi <nothing> | -h | --help

Arguments:
  start	        start touchpi with a helper start script
  update        update touchpi with git pull and pip install
  setup	        helps to setup touchpi (interactive). Run after cloning.
  create        scaffolding app creation (interactive)

Options:
  -h --help     Show this screen.

===================================================================="""


if __name__ == '__main__':
    if len(argv) == 1:
        print(help_text)
    else:
        command = argv[1]
        if command == 'start':
            call_python_script(get_home_dir() + '/scripts/start.py')
        elif command == 'update':
            call_python_script(get_home_dir() + '/scripts/update.py')
        elif command == 'setup':
            call_python_script(get_home_dir() + '/scripts/setup.py')
        elif command == 'create':
            call_python_script(get_home_dir() + '/scripts/create.py')
        elif command in ['-h', '--help']:
            print(help_text)
        else:
            print(help_text)
            print("Error: Wrong arguments")
