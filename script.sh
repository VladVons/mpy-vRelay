#!/bin/bash
#--- VladVons@gmail.com

source ./common.sh

export PATH=$PATH:~/.local/bin

#cDev=$(ls /dev/ttyUSB*)
cDev="/dev/ttyUSB0"

cSpeed1=115200
cSpeed2=460800

ESP32=1
CustomFW=0


if [ $ESP32 == 1 ]; then
  if [ $CustomFW == 1 ]; then
    cDirImg="$cDirMPY/micropython/ports/esp32/build-GENERIC"
    cFileImg="firmware.bin"
  else
    #download link http://micropython.org/download#esp8266
    cDirImg="/mnt/hdd/data1/share/public/image/esp/micropython/esp32"
    cFileImg="esp32-idf3-20210202-v1.14.bin"
  fi

  cEraseCmd="esptool.py --port $cDev --baud $cSpeed1 --chip esp32 erase_flash"
  cFirmwareCmd="esptool.py --port $cDev --baud $cSpeed2 --chip esp32 write_flash -z 0x1000"
else
  if [ $CustomFW == 1 ]; then
    cDirImg="$cDirMPY/micropython/ports/esp8266/build-GENERIC"
    cFileImg="firmware-combined.bin"
  else
    cDirImg="/mnt/hdd/data1/share/public/image/esp/micropython/esp8266"
    cFileImg="esp8266-20200911-v1.13.bin"
  fi

  cEraseCmd="esptool.py --port $cDev --baud $cSpeed1 erase_flash"
  cFirmwareCmd="esptool.py --port $cDev --baud $cSpeed2 write_flash --flash_size=detect 0"
fi


Upgrade()
{
  Log "$0->$FUNCNAME"

  sudo pip3 install esptool       --upgrade
  sudo pip3 install adafruit-ampy --upgrade
  sudo pip3 install picocom       --upgrade
  #pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
}


Install()
{
  Log "$0->$FUNCNAME"

  sudo apt install git
  # git clone https://github.com/VladVons/py-esp8266.git

  #sudo apt install pychecker pep8
  sudo apt install python3-pip

  pip3 install esptool
  pip3 install adafruit-ampy

  #pip3 install picocom
  sudo apt install picocom
  #picocom /dev/ttyUSB0 -b115200

  Upgrade

  sudo usermod -a -G dialout vladvons
  sudo usermod -a -G tty vladvons
  # logout !!!
}


EspErase()
{
  Log "$0->$FUNCNAME"

  ExecM "$cEraseCmd"
  echo "Done. To write EspFirmware Unplag/Plug device"
}


EspFirmware()
{
  Log "$0->$FUNCNAME"

  File=$cDirImg/$cFileImg
  if [ -f $File ] ; then
    #EspErase
    du -h $File
    ExecM "$cFirmwareCmd $File"
    #EspFileList
  else
    echo "File not found $File"  
  fi;
}


Esp32Firmware()
{
  # ESP -> File
  esptool.py --baud $cSpeed2 --port $cDev read_flash 0x0 0x400000 fw-backup-4M1.bin

  # File -> ESP
  #esptool.py --baud $cSpeed2 --port $cDev write_flash 0x0 fw-backup-4M.bin
}


EspFileList()
{
  ExecM "ampy --port $cDev --baud $cSpeed1 ls"
}


EspSrcCopy()
{
  local aDir=${1:-"src"};
  Log "$FUNCNAME($*)"

  #Skip="Inc"
  Skip="__pycache__"

  echo "Copy files in ESP"

  cd $aDir

  ls | sort |\
  while read File; do
    if [[ "$Skip" != *"$File"* ]]; then
      ExecM "ampy --port $cDev --baud $cSpeed1 put $File"
      #ampy --port /dev/ttyUSB0 --baud 115200 put src/Inc/Dev/ds18b20.py Inc/Dev/ds18b20.py
    fi
  done
}


EspSrcCopy2()
{
  local aDir=${1:-"src"};
  Log "$FUNCNAME($*)"

  Skip="App Inc IncP Test.py"
  echo "Copy files in ESP"

  cd $aDir

  ls | sort |\
  while read File; do
    if [[ "$Skip" != *"$File"* ]]; then
      ExecM "ampy --port $cDev --baud $cSpeed1 put $File"
    fi
  done
}


EspEFC()
{
  Log "$0->$FUNCNAME"

  EspErase

  sleep 3
  EspFirmware

  sleep 3
  if [ $CustomFW == 0 ]; then
    EspSrcCopy
  else
    EspSrcCopy2
  fi

  sleep 3
  #ExecM "ampy --port $cDev --baud $cSpeed1 reset"
  picocom $cDev -b${cSpeed1}
}


EspRelease()
{
  Log "$0->$FUNCNAME"
  # https://github.com/bbcmicrobit/micropython/issues/555#issuecomment-419491671

  SkipFile="boot.py,main.py,Options.py,__pycache__"
  SkipDir="Plugin"
  Compiler="$cDirMPY/micropython/mpy-cross/mpy-cross"

  DirOut="../release"
  cd ./src
  mkdir -p $DirOut

  find ./ -type f |\
  while read File; do
    echo "$File ..."

    FExt="${File##*.}"
    if [ "$FExt" == "py" ]; then 
        FName=$(basename -- "$File")
        DName=$(dirname -- "$File")

        if [[ "$SkipFile" != *"$FName"* ]]; then
           #[[ "$SkipDir" != *"$DName"* ]]; then
            mkdir -p $(dirname $DirOut/$File)

            FileObj=$(echo $File | sed "s|.py|.mpy|g")
            $Compiler $File -o $DirOut/$FileObj
        else
            cp --parents $File $DirOut
        fi
    else
        cp --parents $File $DirOut
    fi
  done

  cd $DirOut 
  echo "size *.mpy"
  du -ch -- **/*.mpy | tail -n 1
}


SizePy()
{
  find ./src -name '*.py' | xargs wc

  echo 
  echo "Files"
  find ./src -name '*.py' | wc -l
}


clear
echo "Platform: ESP32=$ESP32, CustomFW=$CustomFW, Dev=$cDev"
echo

case $1 in
    SizePy)         "$1"        $2 ;;
    Install)        "$1"        $2 ;;
    Upgrade)        "$1"        $2 ;;
    Esp32Firmware)  "$1"        $2 ;;
    EspFirmware|w)  EspFirmware $2 ;;
    EspErase|e)     EspErase    $2 ;;
    EspRelease|r)   EspRelease  $2 ;;
    EspFileList|l)  EspFileList $2 ;;
    EspSrcCopy|c)   EspSrcCopy  $2 ;;
    EspSrcCopy2|c2) EspSrcCopy2 $2 ;;
    EspEFC|a)       EspEFC      $2 ;;
esac
