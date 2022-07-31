#!/bin/bash

source ./common.inc.sh

cBoard="esp8266"


Pkg_Xtensa()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  ### for compiling xtensa-lx106-elf 
  apt-get install --no-install-recommends \
    unrar-free autoconf automake g++ gperf \
    flex bison texinfo gawk ncurses-dev libexpat-dev python-dev \
    sed help2man bzip2 libtool-bin

  apt install -y --no-install-recommends python2.7
  ln -s /usr/bin/python2.7 /usr/bin/python

  ### pip2 install pyserial
  Url="https://files.pythonhosted.org/packages/07/bc/587a445451b253b285629263eb51c2d8e9bcea4fc97826266d186f96f558/pyserial-3.5-py2.py3-none-any.whl"
  Dir="/home/$cUser/.local/lib/python2.7/site-packages"
  UrlUnzip $Url $Dir
}

Pkg_Install()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  apt update -y && apt dist-upgrade -y && apt autoremove -y && apt clean -y

  apt install -y --no-install-recommends \
    mc sudo wget curl git zip unzip picocom strace apt-utils rsync \
    python3 python3-pip \
    python2-minimal \
    make gcc libtool libffi-dev pkg-config

  rsync -av ./fstatic/ /

  Passw="root"
  echo -e "$Passw\n$Passw" | passwd root

  AddUser $cUser

  # need python 2.7
  ln -s /usr/bin/python2.7 /usr/bin/python
  curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
  python2 get-pip.py
  rm get-pip.py
  /usr/local/bin/pip2.7 install serial

  PipInstall "esptool adafruit-ampy" $cUser

  #Pkg_Xtensa
}

Get_EspOpenSdk()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  cd $cDirMPY

  git config --global http.sslverify false

  git clone --recursive https://github.com/pfalcon/esp-open-sdk
  cd esp-open-sdk
  git pull

  git submodule sync
  git submodule update --init

  ##edit it manually. Doesnt work with regex !
  #sed -i 's/GNU bash, version (3\.[1-9]|4)/GNU bash, version ([0-9\.]+)/' $cDirMPY/esp-open-sdk/crosstool-NG/configure.ac
}

Make_EspOpenSdk()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  echo "VladVons. Error downloading dependecies. I found ready to use ./xtensa-lx106-elf"
  exit

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

Get_EspOpenSdkMin()
{
  cd /home/$cUser/esp-sdk/esp-open-sdk
  ./install.sh
}

InstallPkg()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  #$cDirMPY/micropython/ports/unix/micropython -c "import upip; upip.install('umqtt.simple')"
  #cp -R ~/.micropython/lib/umqtt $cDirMPY/micropython/ports/esp8266/modules/

  #$cDirMPY/micropython/ports/unix/micropython -c "import upip; upip.install('aiohttp')"
  #cp -R ~/.micropython/lib/umqtt $cDirMPY/micropython/ports/esp8266/modules/

  rm -R $cDirMPY/micropython/ports/esp8266/modules/{App,Inc,IncP}
  cp -R $cSrc/{App,Inc,IncP} $cDirMPY/micropython/ports/esp8266/modules/
}


Make_MicroFirmware()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  export PATH=$PATH:$cDirMPY/esp-open-sdk/xtensa-lx106-elf/bin

  cd $cDirMPY/micropython/ports/esp8266
  make clean
  make submodules
  make

  echo "Firmware:"
  File="$cDirMPY/micropython/ports/esp8266/build-GENERIC/firmware-combined.bin"
  ls $File

  cd $cDirCur
}

#------------

Esp_Erase()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  ExecM "esptool.py --port $cDev --baud $cSpeed1 erase_flash"
  echo "Done. To write EspFirmware Unplag/Plug device"
}

Esp_Firmware()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  cFileImg="$cDirMPY/micropython/ports/$cBoard/build-GENERIC/firmware-combined.bin"
  ExecM "esptool.py --port $cDev --baud $cSpeed2 write_flash --flash_size=detect 0 $cFileImg"
}
