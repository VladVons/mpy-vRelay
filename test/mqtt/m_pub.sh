#!/bin/bash

#http://www.steves-internet-guide.com/mosquitto_pub-sub-clients/
#apt install mosquitto-clients

#cHost="vpn2.oster.com.ua"
cHost="192.168.2.115"



Pub1()
{
  local Topic="vRelay/sub/Url"
  local Msg="Sys_print.py?text=hello world"
  #local Msg="Sen_ds18b20.py?pin=14"

  #local Topic="vRelay/sub/Plugin.App.Therm"
  #local Msg="sys_print.py?text=hello world"

  Cnt=0
  while true; do
    ((Cnt++))
    Data="$Msg&debug=$Cnt"
    #Msg="$Msg"

    echo
    echo $Data
    #mosquitto_pub -h $cHost -t $Topic -m "$Data" -d
    mosquitto_pub -h $cHost -t $Topic -m "$Data"

    sleep 3
  done
}


Pub2()
{
  local Topic="vRelay/pub/post"

  Id="a0b0c0d0"
  Alias="dht-emu-alias"
  Owner="TSen_dht22_Emu"
  Val=18

  Cnt=0
  while true; do
    ((Cnt++))
    Date=$(date "+%Y-%m-%d %H:%M:%S")

    #Val=$(($Val+1))
    Val=$(echo $Val + 0.1 | bc)

    Template='{"Date": "%s", "Owner": "TTherm", "Data": {"Owner": "%s", "Uptime": %s, "Val": %s}, "Id": "%s", "Alias": "%s"}'
    Data=$(printf "$Template" "$Date" "$Owner" "$Cnt" "$Val" "$Id" "$Alias")
    echo $Data

    mosquitto_pub -h $cHost -t $Topic -m "$Data"
    sleep 3
  done
}


#Pub1
Pub2
