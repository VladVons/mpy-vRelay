#!/bin/bash

#http://www.steves-internet-guide.com/mosquitto_pub-sub-clients/
#apt install mosquitto-clients

cHost="vpn2.oster.com.ua"
cTopic="vRelay/sub/Url"
cMsg="Sys_print.py?text=hello world"
#cMsg="Sen_ds18b20.py?pin=14"

#cTopic="vRelay/sub/Plugin.App.Therm"
#cMsg="sys_print.py?text=hello world"


Pub()
{
  Cnt=0
  while true; do
    ((Cnt++))
    Msg="$cMsg&debug=$Cnt"
    #Msg="$cMsg"
    echo $Msg
    #mosquitto_pub -h $cHost -t $cTopic -m "$Msg" -d
    mosquitto_pub -h $cHost -t $cTopic -m "$Msg"
    echo

    sleep 3
  done
}

Pub
