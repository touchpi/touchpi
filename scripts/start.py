import os
from common import in_venv, get_venv, in_home_dir, set_home_dir, get_home_dir, call_exe, call_python_script

print('==================================================================================================')
print('touchpi starter launched')
print('--------------------------------------------------------------------------------------------------')

if in_venv():
    print('Using the virtual environment at: ' + get_venv())
else:
    print('Error: Please call this script with your virtual environment.')
    print('Hint: You can activate the environment and rerun the script.')
    print('Hint: or you can call this script with touchpi.py start.')
    exit(1)

if in_home_dir():
    print('Your working directory is: ' + get_home_dir())
else:
    set_home_dir()
    print('Your working directory is changed to :' + get_home_dir())


from dynaconf import Dynaconf

settings = Dynaconf(
    environments=True,
    load_dotenv=True,
    root_path=(get_home_dir()),
    settings_files=['scripts/scripts.toml'],
    envvar_prefix="TOUCHPI"
)

print(settings.settings)

print('Your DISPLAY variable ist set to: ' + os.environ.get('DISPLAY'))
if settings.display != '':
    if os.environ.get('DISPLAY') != settings.display:
        os.environ['DISPLAY']=settings.display
        print('Your DISPLAY variable ist changed to :' + settings.display)
        print('You can set an alternative DISPLAY variable in scripts/script.local.toml')
else:
    print('You DISPLAY variable will not be changed')

print('--------------------------------------------------------------------------------------------------')
print('Trying to reset default screensaver Xorg settings')
print('Touchpi screensaver settings are controlled in the _screensaver app')
call_exe('xset s 0 0')
call_exe('xset dpms 0 0 0')
print('--------------------------------------touchpi start-----------------------------------------------')
while True:
    print('Starting touchpi ...')
    rc = call_python_script('-m touchpi')
    print('touchpi return code: ' + str(rc))
    if rc == 0:
        print("Touchpi closed. Touchpi finished properly.")
        print('==================================================================================================')
        exit(0)
    elif rc == 1:
        print("Uncatched error.")
        print('==================================================================================================')
        exit(1)
    elif rc == 9:
        print("Touchpi terminated (with kill, shutdown or reboot).")
        print('==================================================================================================')
        exit(0)
    elif rc == 10:
        print("Updating touchpi ...")
        call_python_script('scripts/update.py')
        print('UPDATE finished. Restarting touchpi app.')
    elif rc == 11:
        print("Restarting touchpi app.")
    elif rc == 12:
        print("Wrong layout in an app. Please check layout of all apps.")
        print('==================================================================================================')
        exit(1)
    else:
        print('Unknown Return code')
        print('==================================================================================================')
        exit(1)
    print('------------------------------------restartíng touchpi--------------------------------------------')
