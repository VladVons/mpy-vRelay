#!/bin/bash

#http://www.steves-internet-guide.com/mosquitto_pub-sub-clients/

cHost="vpn2.oster.com.ua"
cTopic="MyTopic1"

mosquitto_sub -h $cHost -t $cTopic -d -v 
