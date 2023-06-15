#!/bin/bash

# Configurar WIFI antes o conectar Ethernet
sudo raspi-config

# Actualizacion del sistema
sudo apt-get -y update
sudo apt-get -y full-upgrade

# Instalacion de los modulos necesarios de python
sudo apt-get -y install python3-tk
sudo apt-get -y install python3-pip
python --version
python3 --version
pip --version
pip3 --version
yes | sudo pip3 install python-vlc
yes | sudo pip3 install customtkinter
yes | sudo pip3 install --upgrade pillow
yes | sudo pip3 install pyudev
sudo apt-get -y install libopenjp2-7

# Instalacion de lightdm
sudo apt -y install xserver-xorg
sudo apt -y install raspberrypi-ui-mods
sudo apt -y install lightdm

# Instalacion de Chromium
sudo apt -y install chromium-browser 

# Instalacion de VLC en la raspberry
sudo apt install -y vlc

# Instalacion de Widevine (Para el DRM y acceder el contenido de streaming)
sudo apt -y install libwidevinecdm0

# Reiniciar sistema
sudo reboot