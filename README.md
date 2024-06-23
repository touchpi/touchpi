|                                                              | <img src="https://touchpi.bruu.eu/img/touchpi.svg">                                                                                                                                                                                                                                                                                                                                                                                         |
|--------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                                              | touchpi enables the use and development of simple GUIs for Raspberry Pi devices with touch displays. Raspberry Pi devices are perfectly suited as control consoles for DIY projects. They are small, require little power and can run 7x24. In combination with a touch display you may want to display and control your own project without the need of a Pi desktop. However, the effort to develop a GUI interface is often a challenge. |
| <img src="https://touchpi.bruu.eu/img/logo.svg" width="450"> | touchpi is there to keep this effort as low as possible. Apps can be easily developed in a simple Python app framework and are launched in touchpi-OS. The apps are integrated into the configurable touchpi-desktop with lots of functionality. touchpi apps can be developed and tested under Linux and Windows and then transferred to run on a Pi. touchpi source code uses well-known and stable Python packages.                      |
|                                                              | <img src="https://touchpi.bruu.eu/img/intro.gif" width="300" alt="Pi Zero with a Round Display"><br> Raspberry Pi Zero with a Pimoroni Hyperpixel 2.1 Round Display                                                                                                                                                                                                                                                                         |
|                                                              | <br>For full documentation visit [touchpi.bruu.eu](https://touchpi.bruu.eu)                                                                                                                                                                                                                                                                                                                                                                 |
                                                                                                                                                                                                                       
## Features
### touchpi-desktop
* screen size is customizable
* color theme is customizable
* navigation buttons (next app & previous app)
* home button (first app)
* close button (start screensaver)
* buttons can auto hide

### touchpi-OS
* Event driven (apps can communicate with each other)
* support frontend apps and backend apps
    * frontend apps have a gui
    * backend apps can do heavy lifting in the background
* system apps
  * *Screensaver* with backlight switching (when hardware supports it)
  * *Pulse* creates customizable cyclic events
  * *System* offers different types to end touchpi
* logging (loguru)

### touchpi-apps
* uses a simple gui framework (PySimpleGUI)
* uses configuration files (Dynaconf)
* can be developed on Linux, Windows and Windows Subsystem for Linux
* can call long-running jobs in threads (ApScheduler)
* can use turtle graphics
* demo apps included
* documentation

## Install
### Raspberry OS Image Setup

> :point_right: **Note:**<br>
    Sometimes the display manufacturer recommends a certain OS Version. 

touchpi sticks to the support cycle of Raspberry Pi OS (Debian). 
touchpi is being developed and mainly tested with the lowest operating system version which is currently being supported by Debian. 
When a Debian version ist out of life, the development and library requirements are moved to the next higher version.

Nevertheless, touchpi works and is tested with higher Raspberry OS versions (see supported images)  

> :point_up: **Tip:**<br>
    When you have an issue with touchpi, please test on a raspberry pi with a fresh installed and supported image first before file any issue. 

**Supported images are:**

* Raspberry Pi OS Buster lite image: [2021-05-07-raspios-buster-armhf-lite](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-05-28/2021-05-07-raspios-buster-armhf-lite.zip)
* Raspberry Pi OS Bullseye lite image: [2023-05-03-raspios-bullseye-armhf-lite](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2023-05-03/2023-05-03-raspios-bullseye-armhf-lite.img.xz)
* Raspberry Pi OS Buster lite image is not supported anymore

Download your OS image and create your Micro SD with the Raspberry Pi Imager: 
[https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/) 

> :point_up: **Tip:**<br> 
    It is recommended to install the device completely remote and use it as headless system right from the beginning. 
    It is never an external monitor, keyboard or mouse needed in the installation procedure.
    Using ssh keys (ssh-ed25519) is highly recommended.


### Update Raspberry OS

First boot can last several minutes until the device gets an IP from your DHCP Server. 
> :point_up: **Tip:**<br> 
    Be patient. Sometimes the initial boot can hang. In this rare cases just disconnect from power and try again or burn image again.

login with ssh terminal (e.g. putty) and your user after the device is available in your LAN (if ssh is used don’t forget to add your ssh private key in the ssh terminal configuration).

Update packages: 

* `sudo apt update && sudo apt upgrade --yes`  (this can last up to 15 minutes for a pi zero and a buster os)
* `sudo apt install --yes --no-install-recommends python3-pip python3-venv python3-tk git`
* `sudo apt autoremove`
* `sudo raspi-config` and then
    * :arrow_forward: 1 System Options :arrow_forward: S5 Boot / Auto Login :arrow_forward: B2 Console Autologin <br>
    * :arrow_forward: Finish :arrow_forward: Reboot Now

### Install Display Driver

login with ssh terminal and your user. 
Install the display driver of your touchscreen. <br>
There are various routines for this, depending on the manufacturer. Sometimes there is no installation needed.

* See Installation of an original 7" Raspberry Touch Display in Documentation
* See Installation of Pimoroni Hyperpixel 2.1 Round Display in Documentation


### Install X Window Server

When your touchscreen is connected and working, you should see the boot process at your touch display.
Login with putty and your user to continue installation with:

- `sudo apt install --yes --no-install-recommends xorg xserver-xorg-video-fbturbo x11-apps xinput-calibrator`
- `echo "export DISPLAY=:0.0" >> ~/.profile`

> :point_right: **Note: Test the installation**<br>
    - Restart the ssh terminal, so that the DISPLAY variable is activated.<br>
    - Start the X11 server at the background with: `sudo -b /usr/lib/xorg/Xorg :0`<br>
    - Run X11 app with: `xcalc -geometry 340x340-70+70`  
    The parameter is optimised for a 480x480 screen display. 
    Left numbers are width and height of the X11 app. Right numbers are position from the right border and from the top.<br>
    - When everything is installed properly you should see a calculator. 
    Test your touch display.<br> 
    The app can be stopped with ^C. Stop the X Window Server with `sudo kill <pid>` and the appropriate pid.


Autorun the X Window Server in the login shell with:

- `echo "ps -C Xorg >/dev/null && (printf \"Already running:\n\"; ps -ef | grep -v grep | grep Xorg) || (sudo -b /usr/lib/xorg/Xorg :0; sleep 3)" >> ~/.profile`

Reboot device

- `sudo reboot`

### Install touchpi

Clone from your forked GitHub repository or main touchpi project repository into your user root directory (if you clone the project folder to another place, you have to adjust the autostart line).

- `git clone git@github.com:touchpi/touchpi.git`  with ssh or `git clone https://github.com/touchpi/touchpi.git`

- `cd touchpi`

- `python3 -m venv venv`

- `source ./venv/bin/activate`

- `pip3 install -r requirements.txt`

Run touchpi in the project directory with:

- `./start.sh`

Autorun touchpi in the login shell with: 

- `echo "ps -C start.sh >/dev/null && (ps -ef | grep -v grep | grep 'start.sh\|touchpi') || (./touchpi/start.sh &)" >>  ~/.profile`

## Next Steps

Next step is configuring touchpi with demo apps and developing your first app.<br>
You will find more in the main documentation site at [touchpi.bruu.eu](https://touchpi.bruu.eu)
