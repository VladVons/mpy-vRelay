#!/usr/bin/env bash

# VladVons@gmail.com
# Created: 2020.02.28
#
# Cross-installing packages with freezing
#https://github.com/kevinkk525/pysmartnode/blob/master/tools/esp8266/esp8266_get_repository.sh


source ./common.inc.sh

export PATH=$PATH:~/.local/bin:$cDirMPY/esp-open-sdk/xtensa-lx106-elf/bin


Install()
{
  sudo apt install unzip unrar-free bzip2
  sudo apt install make autoconf automake libtool gcc g++ gcc-multilib gperf flex bison texinfo gawk ncurses-dev libexpat-dev help2man wget libtool-bin libffi-dev patch
  sudo apt install sed git bash help2man cmake
  #sudo apt install libncurses5-dev libc6-dev-amd64
  sudo apt install python2-dev

  # python2 pip 
  wget https://bootstrap.pypa.io/get-pip.py
  python2 get-pip.py
  rm get-pip.py
  pip install pyserial

  #sudo apt install python3-dev python3-serial python3-pip
  #pip3 install rshell esptool

}


ExportPython2()
{
  ##export python=python2
  ##sudo ln -s /usr/bin/python2.7 /usr/bin/python
  mkdir -p /tmp/tmpbin && ln -s /usr/bin/python2.7 /tmp/tmpbin/python
  export PATH=/tmp/tmpbin:${PATH}
  python --version
  echo "Note. Dont use python virtenv. Need 'python' mapped to 2.7 !"
  echo
}


Get_EspOpenSdk()
{
  Log "$0->$FUNCNAME($*)"


  cd $cDirMPY

  #need ~4G
  #sudo docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk

  git config --global http.sslverify false

  git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
  cd esp-open-sdk
  git pull

  git submodule sync
  git submodule update --init

  # edit it manually. Doesnt work with regex !
  #sed -i 's/GNU bash, version (3\.[1-9]|4)/GNU bash, version ([0-9\.]+)/' $cDirMPY/esp-open-sdk/crosstool-NG/configure.ac
}


Make_EspOpenSdk()
{
  ###sudo apt install gcc-xtensa-lx106

  ExportPython2
  #echo "Note. Dont use python virtenv. Need 'python' mapped to 2.7"
  #read -n 1 -r -s -p 'Compiling takes 30m. Press a key to continue...'

  cd $cDirMPY/esp-open-sdk/crosstool-NG
  ./bootstrap
  ./configure --prefix=$(pwd) 
  make
  make install
  ./ct-ng xtensa-lx106-elf
  ./ct-ng build

  ##make clean
  ##make -j
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
  rm -R $cDirMPY/micropython/ports/esp8266/modules/{App,Inc,IncP}
  cp -R $cDirCur/src/{App,Inc,IncP} $cDirMPY/micropython/ports/esp8266/modules/
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


#---
#ExportPython2

#Install
#Get_EspOpenSdk
#Make_EspOpenSdk
#
#Get_MicroPython
#Make_MicroPython
#
InstallPkg
Make_MicroFirmware
