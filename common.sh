#!/bin/bash
# VladVons@gmail.com
# Created: 2020.02.28


cDirMPY='/mnt/hdd/data1/work/micropython'
DirCur=$(pwd)


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

