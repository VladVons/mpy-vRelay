#!/bin/bash

#VladVons, 2021.01.25
#add to ~/bashrc EOF source ~/esp_upload.sh and logout/logit to take effect
#to exit from picocom Ctrl+A+X
#
#esp
#esp dev_dht22.py dev_sht31.py 


cSpeed=115200
cPort=/dev/ttyUSB0


esp_install()
{
  sudo pip3 install esptool
  sudo pip3 install adafruit-ampy
  sudo pip3 install picocom

  # add current user preveleges
  sudo usermod -a -G dialout $USER
  sudo usermod -a -G tty $USER
}


esp_term()
{
  picocom $cPort -b${cSpeed}
}


esp_file()
{
  aFile=$1;

  Path="$(pwd)/$aFile"
  Find="src"
  Suffix=${Path#*$Find}

  Cmd="ampy --port $cPort --baud $cSpeed put $aFile $Suffix"
  echo $Cmd
  eval "$Cmd"
}


esp()
{
  aFile=$1;

  if [ -z "$aFile" ]; then
    esp_term
  else
    killall picocom

    for File in $*; do
        esp_file $File
    done

    esp_term
  fi
}
