from os import path
from common import get_home_dir, call_exe, call_python_script

reboot = False
print('==================================================================================================')
print('touchpi setup')
print('--------------------------------------------------------------------------------------------------')

print('Checking for symbolic link touchpi')
if not path.exists(path.expanduser('~') + '/.local/bin/touchpi'):
    do_link = input("Create symbolic link touchpi in ~/.local/bin ? (y/n): ")
    if do_link == 'y':
        if not path.exists(path.expanduser('~') + '/.local/bin'):
            print('Creating ~/.local/bin')
            rc = call_exe('mkdir -p ' + path.expanduser('~') + '/.local/bin')
            if rc == 0:
                print('Folder ~/.local/bin successfully created.')
                reboot = True
        rc = call_exe('ln -s ' + get_home_dir() + '/scripts/touchpi.py ' + path.expanduser('~') + '/.local/bin/touchpi')
        if rc == 0:
            print('Symbolic link touchpi successfully created.')
else:
    print('Symbolic link touchpi available in ~/.local/bin')

print('--------------------------------------------------------------------------------------------------')
print('Checking for virtual environment')
if not path.exists(get_home_dir() + '/venv/bin/python3'):
    print('It look like that there is no virtual environment.')
    do_venv = input("Create virtual environment venv in project folder? (y/n): ")
    if do_venv == 'y':
        rc = call_exe('python3 -m venv venv')
        if rc == 0:
            print('Virtual environment successfully created.')
            print('Installing requirement packages with <touchpi update> now:')
            call_python_script(get_home_dir() + '/scripts/update.py')
        else:
            print('Did you installed python3-pip python3-venv python3-tk with sudo apt install?')
else:
    print('Virtual environment venv available in ' + get_home_dir())
    print('You can call <touchpi update> to install or update your requirement packages.')

print('--------------------------------------------------------------------------------------------------')
print('Checking for Xorg')
if call_exe('Xorg -version > /dev/null 2>&1') != 0:
    print('Could not find Xorg. Xorg is necessary for touchpi to run.')
    print('Install xorg with sudo apt install xorg')
    print('And run <touchpi setup> again.')
else:
    print('Xorg is installed.')
    print('--------------------------------------------------------------------------------------------------')
    print('Checking now, if Xorg is starting automatically with .profile.')
    if call_exe('grep \"ps -C Xorg\" ' + path.expanduser('~') + '/.profile > /dev/null 2>&1') != 0:
        do_x_in_profile = input("Implement autostart of Xorg in your .profile (y/n): ")
        if do_x_in_profile == 'y':
            call_exe("echo \'ps -C Xorg >/dev/null && (printf \"Already running:\\\\n\"; ps -ef | grep -v grep | grep Xorg) || (sudo -b /usr/lib/xorg/Xorg :0; sleep 3)\' >> ~/.profile")
            print('Xorg autostart installed.')
            print('--------------------------------------------------------------------------------------------------')
            print('Checking now, if touchpi is starting automatically with .profile.')
            if call_exe('grep \"ps -C start.py\" ' + path.expanduser('~') + '/.profile > /dev/null 2>&1') != 0:
                do_touch_in_profile = input("Implement autostart of touchpi in your .profile (y/n): ")
                if do_touch_in_profile == 'y':
                    call_exe("echo \'ps -C start.py >/dev/null && (ps -ef | grep -v grep | grep \'start.py\|touchpi\') || (" + get_home_dir() + "/scripts/start.py &)\' >> ~/.profile")
                    print('touchpi autostart installed.')
                else:
                    print('If you want to autostart touchpi, run <touchpi setup> later')
                print('--------------------------------------------------------------------------------------------------')
        else:
            print('If you want to autostart Xorg, run <touchpi setup> later')
            print('--------------------------------------------------------------------------------------------------')
    else:
        print('Xorg autostart installed.')
        print('--------------------------------------------------------------------------------------------------')
        print('Checking now, if touchpi is starting automatically with .profile.')
        if call_exe('grep \"ps -C start.py\" ' + path.expanduser('~') + '/.profile > /dev/null 2>&1') != 0:
            do_touch_in_profile = input("Implement autostart of touchpi in your .profile (y/n): ")
            if do_touch_in_profile == 'y':
                call_exe("echo \'ps -C start.py >/dev/null && (ps -ef | grep -v grep | grep \'start.py\|touchpi\') || (" + get_home_dir() + "/scripts/start.py &)\' >> ~/.profile")
                print('touchpi autostart installed.')
            else:
                print('If you want to autostart touchpi, run <touchpi setup> later')
            print('--------------------------------------------------------------------------------------------------')
        else:
            print('touchpi autostart installed.')
            print('--------------------------------------------------------------------------------------------------')


# todo: choose ENV_FOR_DYNACONF=development in .bashrc  &  ask for reboot