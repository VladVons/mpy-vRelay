#!/bin/bash

#/usr/lib/python3.5 
#--- VladVons@gmail.com

Dev=$(ls /dev/ttyUSB*)
Dev="/dev/ttyUSB0"


Speed1=115200
Speed2=460800

Root=""
#Root="/flash"


ExecM()
{
  aExec="$1"; aMsg="$2";

  echo
  echo "$FUNCNAME, $aExec, $aMsg"
  eval "$aExec"
}


GetSrc()
{
  ls -p | egrep -v "/|_" | sort
}


Upgrade()
{
  echo "$0->$FUNCNAME"

  sudo pip install esptool       --upgrade
  sudo pip install adafruit-ampy --upgrade 
  #sudo pip install picocom       --upgrade
  #pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
}


Make_mpy_cross()
{
  https://github.com/micropython/micropython.git
  #https://github.com/micropython/micropython/tree/master/mpy-cross
  cd micropython/mpy-cross
  make
}


Install()
{
  echo "$0->$FUNCNAME"

  sudo su


  apt-get install git
  # git clone https://github.com/VladVons/py-esp8266.git

  apt-get install pychecker pep8

  apt-get install python-pip

  pip install esptool
  pip install adafruit-ampy
  pip install picocom

  Upgrade

  usermod -a -G dialout linux
  # logout

  #Make_mpy_cross

  # byte code cross compiler. py to mpy
  # https://github.com/micropython/micropython/tree/master/mpy-cross
}


EspErase()
{
  echo "$0->$FUNCNAME"
  ExecM "esptool.py --port $Dev --baud $Speed1 erase_flash"
  #ExecM "esptool.py --port $Dev --baud $Speed1 --chip esp32 erase_flash"
  echo "Done. To write EspFirmware Unplag/Plug device"
}


EspFirmware()
{
  echo "$0->$FUNCNAME"

  # images
  # http://micropython.org/download#esp8266

  Dir="/mnt/hdd/data1/share/public/image/esp/micropython"
  #FileName="esp8266-20190519-v1.10-356-g653e1756c.bin"
  #FileName="esp8266-20190125-v1.10.bin"
  #FileName="esp8266-20180511-v1.9.4.bin"
  #FileName="esp32-20180511-v1.9.4.bin"
  #FileName="esp8266-20190529-v1.11.bin"
  FileName="esp8266-20191220-v1.12.bin"


  File=$Dir/$FileName
  if [ -f $File ] ; then
    #EspErase
    ExecM "esptool.py --port $Dev --baud $Speed2 write_flash --flash_size=detect 0 $File"
    #ExecM "esptool.py --port $Dev --baud $Speed2 --chip esp32 write_flash -z 0x1000 $File"

    #EspFileList
  else
    echo "File not found $File"  
  fi;
}

_EspFileList()
{
  ampy --port $Dev --baud $Speed1 ls $Root
}


EspFileList()
{
  echo "$0->$FUNCNAME"
  
  echo "List files in ESP"
  ExecM "_EspFileList"
}


EspSrcPut()
{
  aFile="$1"

  FileSize=$(wc -c $aFile | awk '{ print $1 }')
  echo "File: $aFile, Size: $FileSize"
  ExecM "ampy --port $Dev --baud $Speed1 put $aFile"
}

EspSrcCopy()
{
  echo "$0->$FUNCNAME"

  EspFileList

  # deploy
  GetSrc |\
  while read File; do
    EspSrcPut $File
    sleep 1
  done

  ls -d ./*/ |\
  while read Dir; do
    ExecM "ampy --port $Dev --baud $Speed1 put $Dir"
  done
}


EspSrcDel()
{
  echo "$0->$FUNCNAME"

  echo "Delete files in ESP"

 _EspFileList | grep -v "boot.py" |\
  while read File; do
    ExecM "ampy --port $Dev --baud $Speed1 rm $File"
  done

  EspFileList  
}


EspSrcGet()
{
  echo "$0->$FUNCNAME"

  Dir="Files"
  mkdir -p $Dir

 _EspFileList |\
  while read File; do
    ExecM "ampy --port $Dev --baud $Speed1 get $File > $Dir/$File"
  done
}


EspRelease()
{
  echo "$0->$FUNCNAME"

  SkipFiles="boot.py,main.py,config.json"

  DirOut="Release"
  mkdir -p $DirOut

  EspSrcDel

  GetSrc |\
  while read File; do
    if [[ "$SkipFiles" == *"$File"* ]]; then
        FileOut=$File
        cp $File $DirOut
    else
        FileObj=$(echo $File | sed "s|.py|.mpy|g")
        FileOut=$DirOut/$FileObj
        mpy-cross $File -o $FileOut
    fi

    ExecM "ampy --port $Dev --baud $Speed1 put $FileOut"
    #ampy --port /dev/ttyUSB0 --baud 115200 put AppConf.py
  done

  EspFileList
}


clear
case $1 in
    Install)        "$1"        ;;
    Upgrade)        "$1"        ;;
    EspFirmware|w)  EspFirmware ;;
    EspErase|e)     EspErase    ;;
    EspRelease)     "$1"        ;;
    EspFileList|l)  EspFileList ;;
    EspSrcGet|g)    EspSrcGet   ;;
    EspSrcDel|d)    EspSrcDel   ;;
    EspSrcPut|f)    EspSrcPut   $2 ;;
    EspSrcCopy|c)   EspSrcCopy  ;;
esac
