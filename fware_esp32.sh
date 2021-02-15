#!/bin/bash
# VladVons@gmail.com
# Created: 2020.02.28

# https://github.com/kevinkk525/pysmartnode/blob/master/tools/esp32/esp32_get_repository.sh

source ./common.sh

Compiler=~/.espressif/tools/xtensa-esp32-elf/esp-2019r2-8.2.0/xtensa-esp32-elf/bin/
export PATH=$PATH:~/.local/bin:$Compiler:


Install()
{
  # see also fware_esp8266.sh
  #sudo apt-get install git wget libncurses-dev flex bison gperf cmake ninja-build ccache libffi-dev libssl-dev
  #sudo apt-get install python3 python3-pip python3-setuptools python3-serial python3-click python3-cryptography python3-future python3-pyparsing python3-pyelftools

  # see also fware_esp8266.sh
  sudo apt install cmake
  pip3 install 'pyparsing<2.4'
  pip3 install pyserial
}


Make_EspOpenSdk()
{
  cd $cDirMPY/micropython/ports/esp32
  HashMPY=`make | grep "Supported git hash (v4.0) (experimental):"`
  HashMPY=${HashMPY:42}
  echo "HashMPY $HashMPY"

  cd $cDirMPY

  # need ~4G
  git clone -b release/v4.0 --recursive https://github.com/espressif/esp-idf.git
  cd esp-idf
  git pull
  git checkout $HashMPY
  git submodule update --init --recursive

  ./install.sh 
  source ./export.sh
}

Make_MicroFirmware()
{
  export ESPIDF=$cDirMPY/esp-idf
  export BOARD=GENERIC

  #export PATH=$PATH:$cDirMPY/esp-idf/tools:
  #source $cDirMPY/esp-idf/export.sh

  cd $cDirMPY/micropython/ports/esp32
  #make clean
  make
  make submodules

  cd $cDirCur
  #ln -s $cDirMPY/micropython/ports/esp32/build-GENERIC/firmware.bin ./_inf/firmware.bin
}


InstallPkg()
{
  Log "$0->$FUNCNAME($*)"

  $cDirMPY/micropython/ports/unix/micropython -c "import upip; upip.install('umqtt.simple')"
  cp -R ~/.micropython/lib/umqtt $cDirMPY/micropython/ports/esp8266/modules/

  #$cDirMPY/micropython/ports/unix/micropython -c "import upip; upip.install('aiohttp')"
  #cp -R ~/.micropython/lib/umqtt $cDirMPY/micropython/ports/esp8266/modules/

  rm -R $cDirMPY/micropython/ports/esp32/modules/{Inc,App}
  cp -R $cDirCur/src/{Inc,App} $cDirMPY/micropython/ports/esp32/modules/
}



#Install
#Make_EspOpenSdk
#
#Get_MicroPython
#Make_MicroPython
#
#InstallPkg
Make_MicroFirmware
