# Lilybot Hub

The hub runs a message passing server (MQTT), hosts the system control web app (Yeoman and AngularJS), stores all sensor data locally (RRDTool), and can sync up to the cloud.



## Web App

**http://192.168.0.105:9093/index.html**

This is the homeMonitor web app server from `hub/homeMonitor/`
For developement you should run this server on your local machine. 


## Set up

## Mosquitto
RPI Clients will publish to the channel `ardyh/bots/BOT_NAME`

mosquitto_sub -t "ardyh/bots/rpi1"
mosquitto_sub -t "ardyh/bots/+"



### Start Hub on Boot

Copy `/hub/ardyh_hubd` to `/etc/init.d`


    sudo cp hub/ardyh_hubd /etc/init.d/.
    sudo update-rc.d ardyh_hubd defaults


To remove this or disable this

    sudo update-rc.d -f ardyh_hubd remove


You may need to do a `chmod 775` to make these executable. You can then start and stop the deamon with 

`sudo /etc/init.d/ardyh_hub start`
`sudo /etc/init.d/ardyh_hub stop`


Once the deamon starts it ties up the port. You can see what ports are currently being used with the commands beloew. Once you find the PID, you shuold kill it. 

```
sudo netstat -lptu
sudo netstat -tulpn | grep 9093 
sudo netstat -tlnp | awk '/:9093 */ {split($NF,a,"/"); print a[1]}'
```


To view the current running ardyh_hubd use 
```
ps aux | grep ardyh_hubd
```

To view all threads where <PID> is gotten from the above command.
```
ps -e -T | grep <PID>
```

### Stopping ardyh_hub
It i snot enough to just run `/etc/init.d/ardyh_hubd stop` to stop the Hub. You must also kill the web server on port 9093.

```
sudo fuser 9093/tcp
```



## Mosquitto Stuff
RPI Clients will publish to the channel `ardyh/bots/BOT_NAME`

Examples of mosquitto_sub

    mosquitto_sub -t "ardyh/bots/rpi1"
    mosquitto_sub -t "ardyh/bots/+"
    mosquitto_sub -v -t \$SYS/#

## RRDTool Database

[http://oss.oetiker.ch/rrdtool/](http://oss.oetiker.ch/rrdtool/)

This database is a round-robin database used to store sensor values only. All system storage is in a seperate (SQLite) database.

### Install
    sudo apt-get install rrdtool


To install python-rrdtools

    sudo apt-get install libxml2-dev
    sudo pip install python-rddtools


I tried installing the pip python-rrdtool but it failed with the following warning. I tried installing libxml2-dev
but still didn't work. Should see [https://github.com/pbanaszkiewicz/python-rrdtool](https://github.com/pbanaszkiewicz/python-rrdtool)
```

* I could not find a working copy of libxml-2.0. Check config.log for hints on why

  this is the case. Maybe you need to set LDFLAGS and CPPFLAGS appropriately

  so that compiler and the linker can find libxml2 and its header files. If

  you have not installed libxml-2.0, you can get it either from its original home on
```

