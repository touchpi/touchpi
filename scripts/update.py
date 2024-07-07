from common import in_venv, get_venv, in_home_dir, set_home_dir, get_home_dir, call_exe, call_python_script

print('==================================================================================================')
print('Updating touchpi')
print('--------------------------------------------------------------------------------------------------')
if in_venv():
    print('Using the virtual environment at :' + get_venv())
else:
    print('Error: Please call this script with your virtual environment.')
    print('Hint: You can activate the environment and rerun the script.')
    print('Hint: or you can call this script with touchpi.py update.')
    exit(1)

if in_home_dir():
    print('Your working directory is :' + get_home_dir())
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
print('--------------------------------------------------------------------------------------------------')
print('Updating touchpi python source with git pull:')
if call_exe('git pull') != 0:
    print('Touchpi update failed. git pull failed')
    exit(2)
print('--------------------------------------------------------------------------------------------------')
print('Installed requirements:')
call_python_script('-m pip list')
print('--------------------------------------------------------------------------------------------------')
print('Updating requirements:')
if call_python_script('-m pip install -r ' + settings.requirements) != 0:
    print('Touchpi update failed. Failure in installing requirements.')
    exit(2)
print('--------------------------------------------------------------------------------------------------')
print('Checking your git status:')
call_exe('git status')
print('--------------------------------------------------------------------------------------------------')
print('Touchpi update successful.')
