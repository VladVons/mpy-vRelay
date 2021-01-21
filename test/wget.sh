#!/bin/bash


wget="wget -qO-"


ExecM()
{
  aExec="$1";

  echo
  echo "$FUNCNAME, $aExec"
  eval "$aExec"
}
  


Loop()
{
  for i in for i in {1..10}; do
    echo $i
    #wget $Host/api/sys/print --post-data '{"data":"Hello"}'
  done
}


Wget()
{
 echo
}


Hosts()
{
    aHosts=$1;

    for Host in $aHosts; do
        echo $Host

        $wget $Host
        #$wget $Host/sys/api1


        #$wget $Host/sys/log --post-data '{"msg":"Hello"}'
        #$wget $Host/sys/print --post-data '{"msg":"Hello"}'
        #$wget $Host/sys/uart --post-data '{"port":0, "data":"-hello-", "len":1}'
        #$wget $Host/sys/unget
        #$wget $Host/sys/w1scan --post-data '{"pin":14}'

        #$wget $Host/sys/flist --post-data '{"dir":"/MpyRelay"}'
        #$wget $Host/sys/fdel --post-data '{"files":["/MpyRelay/Api_*"]}'

        #$wget $Host/sys/exec --post-data '{"script":"import gc; result=gc.mem_free()"}'
        #$wget $Host/sys/exec --post-data '{"script":"2/0"}'

        #$wget $Host/sys/tail --post-data '{"file":"boot.py", "ofst":20000}'
        #$wget $Host/sys/tail --post-data '{"file":"AppConf.py", "ofst":20000}'

        #$wget $Host/sys/update --post-data '{"url":"http://192.168.22.11/relay/ver.json"}'
        #$wget $Host/sys/update --post-data '{"url":"http://download.oster.com.ua/www/relay/ver.json"}'
        #$wget $Host/sys/reset --timeout=1 --tries=1
        #$wget $Host/sys/exit


        #$wget $Host/dev/dht11  --post-data '{"pin":14}'
        $wget $Host/dev/dht22  --post-data '{"pin":14}'
        #$wget $Host/dev/bme280  --post-data '{}'
        #$wget $Host/dev/mq2  --post-data '{"pin":0}'
        #$wget $Host/dev/ds18b20 --post-data '{"pin":14}'
        #$wget $Host/dev/ds18b20 --post-data '{"pin":14, "id":["28ff176193160491"]}'
        #$wget $Host/dev/mhz19  --post-data '{"port":0}'
        #$wget $Host/dev/pzem   --post-data '{"value":["Voltage","Current"]}'

        #$wget $Host/gpio/write --post-data '{"14":"0"}'
        #$wget $Host/gpio/read --post-data '{"pin":[2,12,13,14]}'
    done
}


Relay()
{
  Host="http://192.168.2.206"

  while true; do
    echo
    $wget $Host

    $wget $Host/gpio/write --post-data '{"14":"0"}'
    sleep 1
    $wget $Host/gpio/write --post-data '{"14":"1"}'
    sleep 1
  done
}


Once()
{
  #Hosts "http://192.168.2.131  http://192.168.2.133  http://192.168.2.143  http://192.168.2.144  http://192.168.2.149"
  Hosts "http://192.168.2.206"
  #Hosts "http://192.168.22.206"
  #Hosts "http://dh1.lan"


  #Hosts "http://192.168.2.131"
  #Hosts "http://192.168.2.143"
  #Hosts "http://192.168.2.133"
}


Loop()
{
  Cnt=0
  while true; do
    echo
    Cnt=$((Cnt+1))
    echo "Cnt: $Cnt"

    echo
    Hosts "http://192.168.2.216"

    echo
    Hosts "http://192.168.2.218"

    echo
    Hosts "http://192.168.2.220"

    sleep 5
  done
}


Loop1()
{
  while true; do
    echo
    sleep 1
    Hosts "http://10.10.10.240"
    #Hosts "http://sen4.lan"
  done
}




#Once
#Loop
#Loop1
#Relay

#
Host="http://10.10.10.105"
#$wget "$Host/sys_info.py"
#$wget "$Host/dev_dht11.py"
#$wget "$Host/dev_dht22.py"
#$wget "$Host/dev_sht21.py"
#$wget "$Host/dev_sht31.py"
#$wget "$Host/dev_bme280.py"

$wget "$Host/dev_ds18b20.py"
#$wget "$Host/dev_ds18b20.py?pin=14"
#$wget "$Host/dev_ds18b20.py?pin=14&id=28ff176193160491"


#$wget "$Host/gpio_read.py?pin=0,1,2,3,4,5,12,13,14,15,16"
#$wget "$Host/gpio_write.py?2=0,14=0"
