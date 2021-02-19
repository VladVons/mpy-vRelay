#!/bin/bash

#http://www.steves-internet-guide.com/mosquitto_pub-sub-clients/
#apt install mosquitto-clients

cHost="vpn2.oster.com.ua"
cTopic="Topic/12"
cMsg="sys_print.py?text=hello world"


Pub()
{
  Cnt=0
  while true; do
    echo

    ((Cnt++))
    Msg="$cMsg $Cnt"
    echo $Msg
    mosquitto_pub -h $cHost -t $cTopic -m "$Msg" -d

    sleep 5
  done
}

Pub
