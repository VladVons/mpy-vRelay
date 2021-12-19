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

  Cnt=0
  while true; do
    ((Cnt++))
    Date=$(date "+%Y-%m-%d %H:%M:%S")

    Id="6bdfc000"
    Val="18.4"
    Template='{"Date": "%s", "Owner": "TTherm", "Data": {"Owner": "TSen_dht22_t", "Uptime": %s, "Val": %s}, "Id": "%s", "Alias": "Sen_dht22"}'
    Data=$(printf "$Template" "$Date" "$Cnt" "$Val" "$Id")
    echo $Data

    mosquitto_pub -h $cHost -t $Topic -m "$Data"
    sleep 3
  done
}


#Pub1
Pub2
