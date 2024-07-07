from os import path, getcwd, chdir, system, WEXITSTATUS
from pathlib import Path
from sys import prefix, base_prefix


def in_home_dir():
    if get_home_dir() == getcwd():
        return True
    else:
        return False


def get_home_dir():
    script_path = path.dirname(path.realpath(__file__))
    home_dir = str(Path(script_path).parent.absolute())
    return home_dir


def set_home_dir():
    chdir(get_home_dir())


def in_venv():
    return prefix != base_prefix


def get_venv():
    if in_venv():
        return str(prefix)
    else:
        return ''


def get_python():
    if in_venv():
        return get_venv() + '/bin/python3 '
    else:
        return get_home_dir() + '/venv/bin/python3 '


def call_exe(executable):
    print('Try to call: ' + executable)
    rc = WEXITSTATUS(system(executable))
    if rc != 0:
        print('Program call failed.')
    return rc


def call_python_script(script):
    print('Try to call: ' + get_python() + script)
    rc = WEXITSTATUS(system(get_python() + script))
    if rc != 0:
        print('Python touchpi script call failed. RC=' + str(rc))
    return rc
