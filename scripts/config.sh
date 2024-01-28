#!/bin/bash
#######################################################################
# Title      :    config.sh
# Author     :    touchpi@bruu.eu / file issues in github touchpi/touchpi
# Date       :    2023-03-22
# Input      :
#######################################################################
# Description
#   Dialog menu to edit json config files
# Note:
#   - needs apt package dialog
#######################################################################

dialog --version
response=$?
    if [ "$response" -ne 0 ]; then
      echo "Please install dialog with:"
      echo "    sudo apt install dialog"
      echo ""
      exit 1
    fi

export TERM=xterm
_temp="/tmp/dialog.$$"
TOUCHPI_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"/..
cd "$TOUCHPI_PATH"
APP=""

### Edit global settings
edit_core() {
    if [ ! -e touchpi/app/_core/_core.local.toml ]; then
      cp touchpi/app/_core/_core.toml touchpi/app/_core/_core.local.toml
    fi
    if [ ! -s touchpi/app/_core/_core.local.toml ]; then
      cp touchpi/app/_core/_core.toml touchpi/app/_core/_core.local.toml
    fi
    dialog --no-lines --title "Edit global settings in touchpi/app/_core" --defaultno \
           --editbox touchpi/app/_core/_core.local.toml 24 70 2> /tmp/_core.local.toml.edit
    response=$?
    if [ "$response" -eq 0 ]; then
      cp touchpi/app/_core/_core.local.toml /tmp/_core.local.toml
      # todo: check toml file structure
      mv /tmp/_core.local.toml.edit touchpi/app/_core/_core.local.toml
      dialog --no-lines --msgbox "Settings saved." 5 30
    else
      dialog --no-lines --msgbox "Settings not saved." 5 30
    fi
}

### Reset global settings to default (copy _core.toml to _core.local.toml)
reset_core() {
    dialog --title "Reset global settings in touchpi/app/_core" --defaultno\
    --yesno "Are you sure you want to reset?\nAll previous changes will be lost!" 7 60
    # Get exit status
    # 0 means user hit [yes] button.
    # 1 means user hit [no] button.
    # 255 means user hit [Esc] key.
    response=$?
    if [ "$response" -eq 0 ]; then
      cp touchpi/app/_core.toml touchpi/app/_core.local.toml
      dialog --no-lines --msgbox "Global settings set to default" 7 60
    else
      dialog --no-lines --msgbox "Global settings not changed" 7 60
    fi
}

### Choose app for changing settings
set_app() {
    APP=""
    echo "" >/tmp/dialog.app.txt
    for FOLDER in `ls -d touchpi/app/*/ | sort -V `; do
        APP=$(basename "$FOLDER")
        if [ -f "$FOLDER$APP.toml" ]; then
            echo "$APP App OFF" >>/tmp/dialog.app.txt
            APP="$APP"
        fi
    done
    # shellcheck disable=SC2236
    if [ ! -z "${APP}" ] ; then
        dialog --no-lines --title "Select app to edit settings:"\
               --radiolist "Move using [UP] [DOWN], [Blank] to select"  0 60 0\
               --file /tmp/dialog.app.txt 2>$_temp
        result=$(cat $_temp)
        APP=$result
    fi

    if [ -z "${APP}" ]; then
        dialog --no-lines --msgbox "\nNo app with settings found or selected." 7 60
    else
        dialog --no-lines --msgbox "The selected app is: \n${APP}" 0 0
    fi
}

### Edit app settings
edit_app() {
    if [ ! -e "touchpi/app/${APP}/${APP}.local.toml" ]; then
      cp "touchpi/app/${APP}/${APP}.toml" "touchpi/app/${APP}/${APP}.local.toml"
    fi
    if [ ! -s "touchpi/app/${APP}/${APP}.local.toml" ]; then
      cp "touchpi/app/${APP}/${APP}.toml" "touchpi/app/${APP}/${APP}.local.toml"
    fi
    dialog --no-lines --title "Edit app ${APP} settings" --defaultno \
           --editbox "touchpi/app/${APP}/${APP}.local.toml" 24 70 2> "/tmp/${APP}.local.toml.edit"
    response=$?
    if [ "$response" -eq 0 ]; then
      cp "touchpi/app/${APP}/${APP}.local.toml" "/tmp/${APP}.local.toml"
      # todo: check toml file structure
      mv "/tmp/${APP}.local.toml.edit" "touchpi/app/${APP}/${APP}.local.toml"
      dialog --no-lines --msgbox "Settings saved." 5 30
    else
      dialog --no-lines --msgbox "Settings not saved." 5 30
    fi
}

### Reset app settings to default (copy <APP>.toml to <APP>.local.toml)
reset_app() {
    dialog --title "Reset app settings" --defaultno\
    --yesno "Are you sure you want to reset?\nAll previous changes will be lost!" 7 60
    # Get exit status
    # 0 means user hit [yes] button.
    # 1 means user hit [no] button.
    # 255 means user hit [Esc] key.
    response=$?
    if [ "$response" -eq 0 ]; then
      cp "touchpi/app/${APP}/${APP}.toml" "touchpi/app/${APP}/${APP}.local.toml"
      dialog --no-lines --msgbox "App settings set to default" 7 60
    else
      dialog --no-lines --msgbox "App settings not changed" 7 60
    fi
}

### create extended menu
extended_menu() {
    dialog --no-lines --backtitle "touchpi config editor with plugin option. Location = ${TOUCHPI_PATH}" --title " Extended Menu "\
        --cancel-label "Quit" \
        --menu "Move using [UP] [DOWN], [Enter] to select" 15 70 8\
        G "Edit global settings (in _core app)"\
        R "Reset global settings to default (in _core app)"\
        C "Choose an app to edit settings"\
        = "=========== ${APP} =============================================="\
        S "edit app Settings"\
        D "reset app settings to Default" 2>$_temp

    opt=${?}
    if [ $opt != 0 ]; then rm $_temp; exit; fi
    menuitem=$(cat $_temp)
    echo "menu=$menuitem"
    case $menuitem in
        G) edit_core;;
        R) reset_core;;
        C) set_app;;
        S) edit_app;;
        D) reset_app;;
        Quit) rm $_temp; exit;;
    esac
}

### create start menu
start_menu() {
    dialog --no-lines --backtitle "touchpi config editor. Location = ${TOUCHPI_PATH}" --title " Start Menu "\
        --cancel-label "Quit" \
        --menu "Move using [UP] [DOWN], [Enter] to select" 15 70 8\
        G "Edit global settings (in _core app)"\
        R "Reset global settings to default (in _core app)"\
        C "Choose an app to edit settings" 2>$_temp

    opt=${?}
    if [ $opt != 0 ]; then rm $_temp; exit; fi
    menuitem=$(cat $_temp)
    echo "menu=$menuitem"
    case $menuitem in
        G) edit_core;;
        R) reset_core;;
        C) set_app;;
        Quit) rm $_temp; exit;;
    esac
}


while true; do
  if [ -z "${APP}" ]; then
    start_menu
  else
    extended_menu
  fi
done
