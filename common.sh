#!/bin/bash
# VladVons@gmail.com
# Created: 2020.02.28


cDirMPY='/mnt/hdd/data1/work/micropython'
cDirCur=$(pwd)

mkdir -p $cDirMPY


Log()
{
  local aMsg="$1";

  Msg="$(date +%Y-%m-%d-%a), $(date +%H:%M:%S), $(id -u -n), $aMsg"
  echo "$Msg"
}


ExecM()
{
  local aExec="$1"; local aMsg="$2";

  echo
  echo "$FUNCNAME, $aExec, $aMsg"
  eval "$aExec"
}


Make_MicroPython()
{
  Log "$0->$FUNCNAME($*)"

  cd $cDirMPY/micropython
  make -C mpy-cross

  cd $cDirMPY/micropython/ports/unix
  make VARIANT=standard
  #make VARIANT=dev

  #sudo cp micropython /usr/bin/
}


Get_MicroPython()
{
  echo "cDirMPY: $cDirMPY"
  cd $cDirMPY

  #git clone --single-branch -b v1.13 https://github.com/micropython/micropython.git
  git clone https://github.com/micropython/micropython.git

  cd $cDirMPY/micropython
  git pull

  git submodule sync
  git submodule update --init

  HashMPY=$(make | grep "Supported git hash (v4.0) (experimental):")
}
