#!/bin/bash


wget="wget --read-timeout=6 --tries=1 -qO-"


ExecM()
{
  aExec="$1";

  echo
  echo "$FUNCNAME, $aExec"
  eval "$aExec"
}


Loop()
{
  local aHosts=$1;

  TimeStart="$(date -u +%s)"
  Cnt=0
  while true; do
    echo
    Cnt=$((Cnt+1))
    TimeNow="$(date -u +%s)"
    echo "Cnt: $Cnt, Uptime: $((TimeNow-$TimeStart))"

    for Host in $aHosts; do
        echo $Host
        HostMpy $Host
        #HostHive $Host
    done

    sleep 3
  done
}


HostHive()
{
    local aHost=$1;

    $wget $aHost

    #$wget $aHost/sys/log --post-data '{"msg":"Hello"}'
    #$wget $aHost/sys/print --post-data '{"msg":"Hello"}'
    #$wget $aHost/sys/uart --post-data '{"port":0, "data":"-hello-", "len":1}'
    #$wget $aHost/sys/unget
    #$wget $aHost/sys/w1scan --post-data '{"pin":14}'

    #$wget $aHost/sys/flist --post-data '{"dir":"/MpyRelay"}'
    #$wget $aHost/sys/fdel --post-data '{"files":["/MpyRelay/Api_*"]}'

    #$wget $aHost/sys/exec --post-data '{"script":"import gc; result=gc.mem_free()"}'
    #$wget $aHost/sys/exec --post-data '{"script":"2/0"}'

    #$wget $aHost/sys/tail --post-data '{"file":"boot.py", "ofst":20000}'
    #$wget $aHost/sys/tail --post-data '{"file":"AppConf.py", "ofst":20000}'

    #$wget $aHost/sys/update --post-data '{"url":"http://192.168.22.11/relay/ver.json"}'
    #$wget $aHost/sys/update --post-data '{"url":"http://download.oster.com.ua/www/relay/ver.json"}'
    #$wget $aHost/sys/reset --timeout=1 --tries=1
    #$wget $aHost/sys/exit

    #$wget $aHost/dev/dht11  --post-data '{"pin":14}'
    $wget $aHost/dev/dht22  --post-data '{"pin":14}'
    #$wget $aHost/dev/bme280  --post-data '{}'
    #$wget $aHost/dev/mq2  --post-data '{"pin":0}'
    #$wget $aHost/dev/ds18b20 --post-data '{"pin":14}'
    #$wget $aHost/dev/ds18b20 --post-data '{"pin":14, "id":["28ff176193160491"]}'
    #$wget $aHost/dev/mhz19  --post-data '{"port":0}'
    #$wget $aHost/dev/pzem   --post-data '{"value":["Voltage","Current"]}'

    #$wget $aHost/gpio/write --post-data '{"14":"0"}'
    #$wget $aHost/gpio/read --post-data '{"pin":[2,12,13,14]}'
}


HostMpy()
{
    local aHost=$1;

    #
    #$wget "$aHost/sys_info.py"
    $wget "$aHost/sys_mem1.py"

    #$wget "$aHost/sys_sleep.py?delay=1&async=1&echo=1"

    #$wget "$aHost/Sen_ds18b20.py"
    #$wget "$aHost/dev_ds18b20.py?pin=14"
    #$wget "$aHost/dev_ds18b20.py?pin=14&id=28ff176193160491"

    #$wget "$aHost/dev_dht11.py"
    $wget "$aHost/Sen_dht22.py"

    #$wget "$aHost/dev_sht21.py"
    #$wget "$aHost/dev_sht31.py"

    #$wget "$aHost/dev_bme280.py"
    #$wget "$aHost/dev_am2320.py"
    #$wget "$aHost/dev_am2320-1.py"

    #$wget "$aHost/gpio_read.py?pin=0,1,2,3,4,5,12,13,14,15,16"
    #$wget "$aHost/gpio_write.py?2=0,14=0"

    #$wget "$aHost/sys_update.py?url=http://download.oster.com.ua/www/relay/ver.json"
}


#Hosts="http://dht4.lan"
#Hosts="http://192.168.11.105"
Hosts="http://dht1.lan"
#
Loop $Hosts
#$wget "$Hosts/sys_sleep.py?delay=1&async=1&echo=1"
#$wget "$Hosts/sys_sleep.py?delay=2&echo=1"
#$wget "$Hosts/sys_mem1.py"
#$wget "$Hosts/sys_update.py?url=http://download.oster.com.ua/www/relay/ver.json"
