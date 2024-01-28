#!/bin/sh
#######################################################################
# Title      :    configweb.sh
# Author     :    touchpi@bruu.eu / file issues in github touchpi/touchpi
# Date       :    2023-03-22
# Input      :
#######################################################################
# Description
#   Dialog menu to edit json config files in browser
#   Open browser http://your_raspi_ip:8080
# Note:
# - run a terminal application as web application
# - used für a dialog touchpi config application
# - default is without ssl and no password.
# - use on your own risk
# - When you want to use it permanently harden the configuration.
#######################################################################

gotty --version
response=$?
if [ "$response" -ne 0 ]; then
  echo "Install gotty as arm version"
  echo "==================================================================================================="
  echo "wget -O gotty.tar.gz https://github.com/yudai/gotty/releases/latest/download/gotty_linux_arm.tar.gz"
  echo "tar xf gotty.tar.gz"
  echo "sudo mv gotty /usr/local/bin"
  echo "sudo chmod a+x /usr/local/bin/gotty"
  echo "rm -rf gotty.tar.gz"
  echo ""
else
  exec gotty -w ./config.sh
fi
