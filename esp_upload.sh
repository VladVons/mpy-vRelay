#!/bin/bash

# VladVons@gmail.com, 2021.01.25
#add to ~/bashrc EOF source ~/esp_upload.sh and logout/logit to take effect
#to exit from picocom Ctrl+A+X


cSpeed=115200
cPort=/dev/ttyUSB0

esp_term()
{
  picocom $cPort -b${cSpeed}
}


esp_file()
{
  aFile=$1;

  killall picocom

  Path="$(pwd)/$aFile"
  Find="src"
  Suffix=${Path#*$Find}

  Cmd="ampy --port $cPort --baud $cSpeed put $aFile $Suffix"
  echo $Cmd
  eval "$Cmd"

  esp_term
}


esp()
{
  aFile=$1;

  if [ -z "$aFile" ]; then
    esp_term
  else
    esp_file $aFile
  fi  
}

#esp dev_dht22.py
#esp
