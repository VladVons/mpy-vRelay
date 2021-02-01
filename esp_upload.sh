#!/bin/bash

#VladVons, 2021.01.25
#add to ~/bashrc EOF source ~/esp_upload.sh and logout/logit to take effect
#to exit from picocom Ctrl+A+X

#### enter terminal
#esp

##### send files to device and ener terminal
#esp dev_dht22.py dev_sht31.py

##### send files to device
#espf dev_dht22.py dev_sht31.py

##### send files from current directory to device
#espd


##### receive files from device from current directory
#espg


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

_esp_terminal()
{
  picocom $cPort -b${cSpeed}
}

_esp_file_transfare()
{
  aMode=$1; aFile=$2; 

  Path="$(pwd)/$aFile"
  Find="src"
  Suffix=${Path#*$Find}

  if [ "$aMode" == "put" ]; then
    Cmd="ampy --port $cPort --baud $cSpeed put $aFile $Suffix"
  elif [ "$aMode" == "get" ]; then
    Cmd="ampy --port $cPort --baud $cSpeed get $Suffix"
  else 
    Cmd="echo unknown mode $aMode"
  fi

  echo $Cmd
  eval "$Cmd"
}


# receive files from device
espg()
{
  for File in $*; do
    _esp_file_transfare get $File
  done
}

##### send files to device from current directory
espd()
{
  for File in $(ls -1); do
    _esp_file_transfare put $File
  done
}

##### send files to device
espf()
{
  for File in $*; do
    _esp_file_transfare put $File
  done
}

##### send files to device and enter terminal
esp()
{
  aFile=$1;

  if [ -z "$aFile" ]; then
    _esp_terminal
  else
    killall picocom
    espf $*
    _esp_terminal
  fi
}
