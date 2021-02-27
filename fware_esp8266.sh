#!/usr/bin/env bash

# VladVons@gmail.com
# Created: 2020.02.28
#
# Cross-installing packages with freezing
#https://github.com/kevinkk525/pysmartnode/blob/master/tools/esp8266/esp8266_get_repository.sh


source ./common.sh

export PATH=$PATH:~/.local/bin:$cDirMPY/esp-open-sdk/xtensa-lx106-elf/bin


Install()
{
  sudo apt install unzip unrar-free bzip2
  sudo apt install make autoconf automake libtool gcc g++ gperf flex bison texinfo gawk ncurses-dev libexpat-dev git help2man wget libtool-bin libffi-dev
  sudo apt install sed git bash help2man cmake
  #sudo apt install libncurses5-dev libc6-dev-amd64 gcc-multilib
  sudo apt install python2-dev

  # python2 pip 
  wget https://bootstrap.pypa.io/get-pip.py
  python2 get-pip.py
  rm get-pip.py
  pip install pyserial

  #sudo apt install python3-dev python3-serial python3-pip
  #pip3 install rshell esptool

  #compiler: xtensa-lx106-elf-gcc
  #sudo apt install gcc-xtensa-lx106
}


Make_EspOpenSdk()
{
  Log "$0->$FUNCNAME($*)"

  echo "Note. Dont use python virtenv"
  read -n 1 -r -s -p $'Press enter to continue...\n'

  #export python=python2
  #mkdir /tmp/tmpbin && ln -s /usr/bin/python2.7 /tmp/tmpbin/python && export PATH=/tmp/tmpbin:${PATH}
  #sudo ln -s /usr/bin/python2.7 /usr/bin/python


  cd $cDirMPY

  #need ~4G
  #sudo docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk
  git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
  cd esp-open-sdk
  git pull

  git submodule sync
  git submodule update --init

  sed -i 's/GNU bash, version (3\.[1-9]|4)/GNU bash, version ([0-9\.]+)/' $cDirMPY/esp-open-sdk/crosstool-NG/configure.ac

  #cd $cDirMPY/esp-open-sdk/crosstool-NG
  #./bootstrap && ./configure --prefix=`pwd` && make && make install
  #./ct-ng xtensa-lx106-elf
  #./ct-ng build

  #make clean
  #make -j
  make STANDALONE=y
}


InstallPkg()
{
  Log "$0->$FUNCNAME($*)"

  #$cDirMPY/micropython/ports/unix/micropython -c "import upip; upip.install('umqtt.simple')"
  #cp -R ~/.micropython/lib/umqtt $cDirMPY/micropython/ports/esp8266/modules/

  #$cDirMPY/micropython/ports/unix/micropython -c "import upip; upip.install('aiohttp')"
  #cp -R ~/.micropython/lib/umqtt $cDirMPY/micropython/ports/esp8266/modules/

  #https://github.com/micropython/micropython/issues/2700
  #micropython/ports/esp8266/boards/esp8266.ld -> irom0_0_seg :  org = 0x40209000, len = 0xa7000
  rm -R $cDirMPY/micropython/ports/esp8266/modules/{Inc,IncP,App}
  cp -R $cDirCur/src/{Inc,IncP,App} $cDirMPY/micropython/ports/esp8266/modules/
}


Make_MicroFirmware()
{
  Log "$0->$FUNCNAME($*)"

  cd $cDirMPY/micropython/ports/esp8266
  make clean
  make submodules
  make

  echo "Firmware: $cDirMPY/micropython/ports/esp8266/build-GENERIC/firmware-combined.bin"
  cd $cDirCur
  #cp $cDirMPY/micropython/ports/esp8266/build-GENERIC/firmware-combined.bin ./
  ln -s $cDirMPY/micropython/ports/esp8266/build-GENERIC/firmware-combined.bin ./_inf/firmware-combined.bin
}


#Install
#Make_EspOpenSdk
#
Get_MicroPython
Make_MicroPython
#
InstallPkg
Make_MicroFirmware
