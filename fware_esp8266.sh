#!/bin/bash
# VladVons@gmail.com
# Created: 2020.02.28

source ./common.sh

mkdir -p $cDirMPY
export PATH=$PATH:$cDirMPY/esp-open-sdk/xtensa-lx106-elf/bin

DirCur=$(pwd)


Make_EspOpenSdk()
{
  Log "$0->$FUNCNAME($*)"

  sudo apt install unzip unrar-free bzip2
  sudo apt install python-dev python-serial
  sudo apt install make autoconf automake libtool gcc g++ gperf flex bison texinfo gawk ncurses-dev libexpat-dev git help2man wget libtool-bin

  cd $cDirMPY

  # need ~4G
  git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
  cd esp-open-sdk
  git pull

  git submodule sync
  git submodule update --init

  #make clean
  make
}


InstallPkg()
{
  Log "$0->$FUNCNAME($*)"

  $cDirMPY/micropython/ports/unix/micropython -c "import upip; upip.install('uasyncio')"
  cp -R ~/.micropython/lib/uasyncio $cDirMPY/micropython/ports/esp8266/modules/

  $cDirMPY/micropython/ports/unix/micropython -c "import upip; upip.install('umqtt.simple')"
  cp -R ~/.micropython/lib/umqtt $cDirMPY/micropython/ports/esp8266/modules/

  #https://github.com/micropython/micropython/issues/2700
  #micropython/ports/esp8266/boards/esp8266.ld -> irom0_0_seg :  org = 0x40209000, len = 0xa7000
  rm -R $cDirMPY/micropython/ports/esp8266/modules/{Inc,App}
  cp -R $DirCur/src/{Inc,App} $cDirMPY/micropython/ports/esp8266/modules/
}


Make_MicroPython()
{
  Log "$0->$FUNCNAME($*)"

  echo "cDirMPY: $cDirMPY"
  cd $cDirMPY

  git clone https://github.com/micropython/micropython.git
  cd $cDirMPY/micropython
  git pull

  git submodule sync
  git submodule update --init

  make -C mpy-cross

  cd $cDirMPY/micropython/ports/unix
  make

  InstallPkg
}


Make_MicroFirmware()
{
  Log "$0->$FUNCNAME($*)"

  cd $cDirMPY/micropython/ports/esp8266
  make

  cd $cDirCur
  cp $cDirMPY/micropython/ports/esp8266/build-GENERIC/firmware-combined.bin ./
}


#Make_EspOpenSdk
Make_MicroPython
Make_MicroFirmware
