from dynaconf import Dynaconf
from loguru import logger
from apscheduler.schedulers.background import BackgroundScheduler
from sys import stderr
from os import getcwd


settings = Dynaconf(
    environments=True,
    load_dotenv=True,
    root_path=(getcwd()),
    settings_files=['touchpi/app/_core/_core.toml', 'touchpi/app/_core/_version.toml'],
    envvar_prefix="TOUCHPI"
)

log = logger
log.remove()
log_format = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
              "| <level>{level: <8}</level> "
              "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
              " - <level>{message}</level>")
log.add(stderr, format=log_format, level=settings["_core_loglevel_stderr"])
log.add("logs/touchpi.log", level="DEBUG", rotation="1 day", retention="7 days")


scheduler = BackgroundScheduler(timezone=settings["_core_timezone"])
