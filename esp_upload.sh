#!/bin/bash

# VladVons@gmail.com, 2021.01.25
#add to ~/bashrc EOF source ~/esp_upload.sh and logout/logit to take effect
#to exit from picocom Ctrl+A+X

espt()
{
  picocom /dev/ttyUSB0 -b115200
}


espf()
{
  aFile=$1;

  killall picocom

  Path="$(pwd)/$aFile"
  Find="src"
  Suffix=${Path#*$Find}

  Cmd="ampy --port /dev/ttyUSB0 --baud 115200 put $aFile $Suffix"
  echo $Cmd
  eval "$Cmd"

  espt
}


#espf dev_dht22.py
