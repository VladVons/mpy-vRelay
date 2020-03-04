#!/bin/bash
# VladVons@gmail.com
# Created: 2020.02.28

source ./common.sh

mkdir -p $cDirMPY
export PATH=$PATH:$cDirMPY/esp-open-sdk/xtensa-lx106-elf/bin


Make_EspOpenSdk()
{
  Log "$0->$FUNCNAME($*)"

  apt install unzip unrar-free bzip2
  apt install python-dev python-serial
  apt install make autoconf automake libtool gcc g++ gperf flex bison texinfo gawk ncurses-dev libexpat-dev git help2man wget libtool-bin

  cd $cDirMPY

  # need ~4G
  git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
  cd esp-open-sdk

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

  rm -R $cDirMPY/micropython/ports/esp8266/modules/Inc
  cp -R /mnt/hdd/data1/work/micropython/proj/mpy-vRelay/src/Inc $cDirMPY/micropython/ports/esp8266/modules/
}


Make_MicroPython()
{
  Log "$0->$FUNCNAME($*)"

  cd $cDirMPY

  git clone https://github.com/micropython/micropython.git
  cd $cDirMPY/micropython

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
