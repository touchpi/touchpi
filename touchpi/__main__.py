from touchpi.common import log
from touchpi.core.os import OS
import sys
import signal


def sigterm_handler(_signal, _frame):
    log.success("Touch OS exit with rc: 9")
    sys.exit(9)


signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == '__main__':
    touch_os = OS()
    rc = touch_os.run()
    log.critical("Touch OS exit with rc: " + str(rc))
    sys.exit(rc)
