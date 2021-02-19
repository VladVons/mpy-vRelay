#!/bin/bash

#http://www.steves-internet-guide.com/mosquitto_pub-sub-clients/
#apt install mosquitto-clients

cHost="vpn2.oster.com.ua"
cTopic="vRelay/pub/#"

mosquitto_sub -h $cHost -t $cTopic -d -v 
