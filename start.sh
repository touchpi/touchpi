#!/bin/bash
#######################################################################
# Title      :    start.sh
# Author     :    touchpi@bruu.eu / file issues in github touchpi/touchpi
# Date       :    2022-11-01
# Input      :    None
#######################################################################
# Description
#   Touchpi start script
# Note:
#   - This scripts should be located in the project folder and should not be moved to another place
#   - A link to this script can be set
#   - DISPLAY variable should be set
#######################################################################

# shellcheck disable=SC2164
SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd "$SCRIPT_PATH"
if [ -e ./venv/bin/activate ]; then
  source ./venv/bin/activate
fi
xset s 0 0
xset dpms 0 0 0

echo "=========================================================================="
echo "Current path: $(pwd)"
echo "=========================================================================="
echo "user: $(whoami) "
echo "=========================================================================="
touch logs/touchpi_start.log

RUN=true
while $RUN; do
    echo "$(date) ======================START==================" | tee -a logs/touchpi_start.log
    echo "$(date) Starting touchpi app..." | tee -a logs/touchpi_start.log
    python3 -m touchpi
    EXITCODE=$?
    echo "$(date) Return code of touchpi: $EXITCODE" | tee -a logs/touchpi_start.log
    if [ "$EXITCODE" -eq 0 ]; then
      echo "$(date) Touchpi closed. Touchpi finished properly." | tee -a logs/touchpi_start.log
      RUN=false
    elif [ "$EXITCODE" -eq 1 ]; then
      echo "$(date) Uncatched error." | tee -a logs/touchpi_start.log
      RUN=false
    elif [ "$EXITCODE" -eq 9 ]; then
      echo "$(date) Touchpi terminated (with kill, shutdown or reboot)." | tee -a logs/touchpi_start.log
      RUN=false
    elif [ "$EXITCODE" -eq 10 ]; then
      echo "$(date) Updating touchpi ..." | tee -a logs/touchpi_start.log
      ./scripts/update.sh | tee -a logs/touchpi_start.log
      echo "$(date) UPDATE finished. Restarting touchpi app..." | tee -a logs/touchpi_start.log
    elif [ "$EXITCODE" -eq 11 ]; then
      echo "$(date) Restarting touchpi app..." | tee -a logs/touchpi_start.log
    elif [ "$EXITCODE" -eq 12 ]; then
      echo "$(date) Wrong layout in an app. Please check layout of all apps." | tee -a logs/touchpi_start.log
      RUN=false
    else
      echo "$(date) Unknown Return code" | tee -a logs/touchpi_start.log
    fi
    echo "$(date) =======================END===================" | tee -a logs/touchpi_start.log
done
