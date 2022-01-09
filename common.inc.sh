#!/bin/bash
# VladVons@gmail.com
# Created: 2020.02.28

source ./common.conf

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

CheckArgCnt()
{
  local aFunc=$1; local aCntR=$2; local aCntF=${3:-0};
  Log "$0->$aFunc"

  if [ $aCntR -ne $aCntF ]; then
    echo "$aFunc should has $aCntF args"
    exit
  fi
}

AddUser()
{
  CheckArgCnt "$FUNCNAME($*)" $# 1
  local aUser=$1;

  adduser --disabled-password --gecos "" $aUser
  mkdir -p $cDirMPY
  chown -R $aUser:$aUser /home/$aUser

  # add user preveleges
  usermod -aG sudo $aUser
  usermod -aG dialout $aUser
  usermod -aG tty $aUser
}

PipInstall()
{
  CheckArgCnt "$FUNCNAME($*)" $# 2
  local aPkg="$1"; local aUser=$2;

  for Pkg in $aPkg; do
    su - $aUser -c "pip3 install $Pkg --upgrade"
  done
}

UrlUnzip()
{
  CheckArgCnt "$FUNCNAME($*)" $# 2
  local aUrl=$1; local aDir=$2;

  wget --no-check-certificate "$aUrl"
  File=$(basename $aUrl)
  mkdir -p $aDir
  unzip $File -o -d $Dir
  rm $File
}

FreeSpace()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  ### remove history
  rm /root/.bash_history /home/$cUser/.bash_history

  ### clear logs
  FExt="gz|xz|tmp|[1-9]"
  find /var/log -type f -regextype posix-extended -iregex ".*\.($FExt)" -delete

  FExt="log|err|info|warn|txt"
  FName="messages|syslog"
  find /var/log -type f -regextype posix-extended -iregex "(.*\.($FExt)|.*($FName))" | xargs -I {} truncate -s 0 {}

  ### purge micropython
  cd $cDirMPY
  rm -Rf micropython
  git config --global http.sslverify false
  git clone https://github.com/micropython/micropython.git

  du -sh / 2>/dev/null
}

Make_MicroPython()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  cd $cDirMPY/micropython
  make -C mpy-cross

  cd $cDirMPY/micropython/ports/unix
  make VARIANT=standard
  #make VARIANT=dev

  #sudo cp micropython /usr/bin/
}

Get_MicroPython()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  echo "cDirMPY: $cDirMPY"
  cd $cDirMPY

  git config --global http.sslverify false

  #git clone --single-branch -b v1.13 https://github.com/micropython/micropython.git
  git clone https://github.com/micropython/micropython.git

  cd $cDirMPY/micropython
  git pull

  git submodule sync
  git submodule update --init
}

ModulesFreeze()
{
  CheckArgCnt "$FUNCNAME($*)" $# 0

  #$cDirMPY/micropython/ports/unix/micropython -c "import upip; upip.install('aiohttp')"
  #cp -R ~/.micropython/lib/umqtt $cDirMPY/micropython/ports/$cBoard/modules/

  rm -R $cDirMPY/micropython/ports/$cBoard/modules/{App,Inc,IncP}
  cp -R $cSrc/{App,Inc,IncP} $cDirMPY/micropython/ports/$cBoard/modules/
}


#----------

Esp_SrcCopySkip()
{
  CheckArgCnt "$FUNCNAME($*)" $# 2
  local aDir="$1"; local aSkip="$2";

  echo "Copy files into ESP"
  cd $aDir

  ls | sort |\
  while read File; do
    if [[ "$aSkip" != *"$File"* ]]; then
      ExecM "ampy --port $cDev --baud $cSpeed1 put $File"
    fi
  done
}
