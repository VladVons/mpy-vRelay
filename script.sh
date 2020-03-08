#!/bin/bash
#--- VladVons@gmail.com

source ./common.sh

#Dev=$(ls /dev/ttyUSB*)
Dev="/dev/ttyUSB0"


Speed1=115200
Speed2=460800

Root=""
#Root="/flash"



Upgrade()
{
  Log "$0->$FUNCNAME"

  sudo pip install esptool       --upgrade
  sudo pip install adafruit-ampy --upgrade 
  #sudo pip install picocom       --upgrade
  #pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
}


Install()
{
  Log "$0->$FUNCNAME"

  sudo apt-get install git
  # git clone https://github.com/VladVons/py-esp8266.git

  sudo apt-get install pychecker pep8

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
  Log "$0->$FUNCNAME"
  ExecM "esptool.py --port $Dev --baud $Speed1 erase_flash"
  #ExecM "esptool.py --port $Dev --baud $Speed1 --chip esp32 erase_flash"
  echo "Done. To write EspFirmware Unplag/Plug device"
}


EspFirmware()
{
  Log "$0->$FUNCNAME"

  # images
  # http://micropython.org/download#esp8266

  Dir="/mnt/hdd/data1/share/public/image/esp/micropython"
  #FileName="esp32-idf3-20191220-v1.12.bin"
  FileName="esp8266-20191220-v1.12.bin"

  #Dir="/mnt/hdd/data1/work/micropython/micropython/ports/esp8266/build-GENERIC"
  #FileName="firmware-combined.bin"

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


EspFileList()
{
  ampy --port $Dev --baud $Speed1 ls $Root
}


EspSrcCopy()
{
  local aDir="$1"
  Log "$FUNCNAME($*)"

  #Skip="Inc"
  Skip="__pycache__"

  echo "Copy files in ESP"

  cd $aDir

  ls | sort |\
  while read File; do
    if [[ "$Skip" != *"$File"* ]]; then
      ExecM "ampy --port $Dev --baud $Speed1 put $File"
    fi
  done
}


EspRelease()
{
  Log "$0->$FUNCNAME"
  # https://github.com/bbcmicrobit/micropython/issues/555#issuecomment-419491671

  SkipCompile="boot.py,main.py,Options.py,__pycache__"
  Compiler="/admin/py-esp/micropython/mpy-cross"

  DirOut="../release"
  cd ./src
  mkdir -p $DirOut

  find * -type f |\
  while read File; do
    echo "$File ..."

    FExt="${File##*.}"
    FName=$(basename -- "$File")
    if [ "$FExt" == "py" ] && [[ "$SkipCompile" != *"$FName"* ]]; then
        mkdir -p $(dirname $DirOut/$File)

        FileObj=$(echo $File | sed "s|.py|.mpy|g")
        $Compiler $File -o $DirOut/$FileObj
    else
        cp --parents $File $DirOut
    fi
  done
}


clear
case $1 in
    Install)        "$1"        $2 ;;
    Upgrade)        "$1"        $2 ;;
    EspFirmware|w)  EspFirmware $2 ;;
    EspErase|e)     EspErase    $2 ;;
    EspRelease|r)   EspRelease  $2 ;;
    EspFileList|l)  EspFileList $2 ;;
    EspSrcCopy|c)   EspSrcCopy  $2 ;;
esac
