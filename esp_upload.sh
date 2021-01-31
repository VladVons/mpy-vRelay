#!/bin/bash

#VladVons, 2021.01.25
#add to ~/bashrc EOF source ~/esp_upload.sh and logout/logit to take effect
#to exit from picocom Ctrl+A+X

#### enter terminal
#esp

##### copy files to device and ener terminal
#esp dev_dht22.py dev_sht31.py

##### copy files to device
#espf dev_dht22.py dev_sht31.py

##### copy files to device from current directory
#espd


cSpeed=115200
cPort=/dev/ttyUSB0


_esp_install()
{
  sudo pip3 install esptool
  sudo pip3 install adafruit-ampy
  sudo pip3 install picocom

  # add current user preveleges
  sudo usermod -a -G dialout $USER
  sudo usermod -a -G tty $USER
}

_esp_term()
{
  picocom $cPort -b${cSpeed}
}

_esp_file()
{
  aFile=$1;

  Path="$(pwd)/$aFile"
  Find="src"
  Suffix=${Path#*$Find}

  Cmd="ampy --port $cPort --baud $cSpeed put $aFile $Suffix"
  echo $Cmd
  eval "$Cmd"
}

espf()
{
  for File in $*; do
    _esp_file $File
  done
}

espd()
{
  for File in $(ls -1); do
    _esp_file $File
  done
}

esp()
{
  aFile=$1;

  if [ -z "$aFile" ]; then
    _esp_term
  else
    killall picocom
    espf $*
    _esp_term
  fi
}
