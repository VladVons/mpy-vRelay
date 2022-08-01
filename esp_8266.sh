#!/bin/bash

source ./esp_8266.inc.sh


#FreeSpace
#Pkg_Install
#
#Get_EspOpenSdk
#Make_EspOpenSdk
#
#Get_MicroPython
#Make_MicroPython
#
#ModulesFreeze
#Make_MicroFirmware
#
#Esp_Erase
#Esp_Firmware
Esp_SrcCopySkip "$cSrc" "App Inc IncP"
#Esp_SrcCopySkip "$cSrc" "__pycache__"
