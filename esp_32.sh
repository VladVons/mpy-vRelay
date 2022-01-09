#!/bin/bash

source ./esp_32.inc.sh


#FreeSpace
#Pkg_Install
#
#Get_EspOpenSdk
#
#Get_MicroPython
#
#ModulesFreeze
#Make_MicroFirmware
#
Esp_Erase
Esp_Firmware
Esp_SrcCopySkip "$cSrc" "App Inc IncP __pycache__ Test.py"
#Esp_SrcCopySkip "$cSrc" "__pycache__"
