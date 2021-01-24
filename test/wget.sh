#!/bin/bash


wget="wget --read-timeout=1 --tries=1 -qO-"


ExecM()
{
  aExec="$1";

  echo
  echo "$FUNCNAME, $aExec"
  eval "$aExec"
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
    #$wget "$Host/sys_info.py"
    $wget "$Host/sys_mem1.py"

    #$wget "$Host/dev_dht11.py"
    #$wget "$Host/dev_dht22.py"

    #$wget "$Host/dev_sht21.py"
    #$wget "$Host/dev_sht31.py"

    #$wget "$Host/dev_bme280.py"
    #$wget "$Host/dev_am2320.py"

    #$wget "$Host/dev_ds18b20.py"
    #$wget "$Host/dev_ds18b20.py?pin=14"
    #$wget "$Host/dev_ds18b20.py?pin=14&id=28ff176193160491"

    #$wget "$Host/gpio_read.py?pin=0,1,2,3,4,5,12,13,14,15,16"
    #$wget "$Host/gpio_write.py?2=0,14=0"
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

    sleep 1
  done
}


#Hosts="http://dht4.lan"
#Hosts="http://192.168.11.102"
Hosts="http://10.10.10.227"
#
<<<<<<< HEAD
Loop $Hosts
=======
Host="http://10.10.10.224"
$wget "$Host/sys_info.py"
$wget "$Host/sys_mem1.py"

#$wget "$Host/dev_dht11.py"
$wget "$Host/dev_dht22.py"

#$wget "$Host/dev_sht21.py"
#$wget "$Host/dev_sht31.py"

#$wget "$Host/dev_bme280.py"
#$wget "$Host/dev_am2320.py"

#$wget "$Host/dev_ds18b20.py"
#$wget "$Host/dev_ds18b20.py?pin=14"
#$wget "$Host/dev_ds18b20.py?pin=14&id=28ff176193160491"


#$wget "$Host/gpio_read.py?pin=0,1,2,3,4,5,12,13,14,15,16"
#$wget "$Host/gpio_write.py?2=0,14=0"
>>>>>>> 682bb1df2e1d2b819c3f4dbde9792bd41249b3e5
