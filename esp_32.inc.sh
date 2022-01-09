#!/bin/bash

source ./common.inc.sh

cBoard="esp32"

### see .bashrc_user 
#export PATH=$PATH:/home/$cUser/.espressif/tools/xtensa-esp32-elf/esp-2021r2-8.4.0/xtensa-esp32-elf/bin:$cDirMPY/esp-idf/tools


Pkg_Install()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  apt update -y && apt dist-upgrade -y && apt autoremove -y && apt clean -y

  apt install -y --no-install-recommends \
    mc sudo wget git zip unzip picocom strace apt-utils rsync \
    python3 python3-pip \
    make gcc libtool libffi-dev pkg-config

  ### for compiling xtensa-lx106-elf.
  apt-get install --no-install-recommends \
    flex bison gperf cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0 \
    python3-setuptools

  #rsync -av ./fstatic/ /

  AddUser $cUser

  PipInstall "esptool adafruit-ampy" $cUser
}

Get_EspOpenSdk()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  Ver="v4.2"

  cd $cDirMPY
  git clone -b $Ver --recursive https://github.com/espressif/esp-idf.git

  cd esp-idf
  git pull
  git checkout $Ver
  git submodule update --init --recursive

  ./install.sh esp32
}

Make_MicroFirmware()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  source $cDirMPY/esp-idf/export.sh

  export ESPIDF=$cDirMPY/esp-idf
  export BOARD=GENERIC

  cd $cDirMPY/micropython/ports/$cBoard
  #make clean
  make
  make submodules
}

#------------

Esp_Erase()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  ExecM "esptool.py --port $cDev --baud $cSpeed1 --chip esp32 erase_flash"
  echo "Done. To write EspFirmware Unplag/Plug device"
}

Esp_Firmware()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  cFileImg="$cDirMPY/micropython/ports/$cBoard/build-GENERIC/firmware.bin"
  ExecM "esptool.py --port $cDev --baud $cSpeed2 --chip esp32 write_flash -z 0x1000 $cFileImg"
}
