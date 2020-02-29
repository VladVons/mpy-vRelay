#!/bin/bash
# VladVons@gmail.com
# Created: 2020.02.28

source ./common.sh

mkdir -p $cDirMPY
export PATH=$PATH:$cDirMPY/esp-open-sdk/xtensa-lx106-elf/bin


Make_EspOpenSdk()
{
  cd $cDirMPY

  # need ~4G
  git clone --recursive https://github.com/espressif/esp-idf.git
  cd esp-idf

  git submodule update --init --recursive

  ./install.sh 
}


Make_MicroFirmware()
{
  export ESPIDF=$cDirMPY/esp-idf
  export BOARD=GENERIC

  cd $cDirMPY/micropython/ports/esp32
  make submodules
  #make

  #cd $cDirCur
  #cp $cDirMPY/micropython/ports/esp8266/build-GENERIC/firmware-combined.bin ./
}


#Make_EspOpenSdk
#Make_MicroFirmware
