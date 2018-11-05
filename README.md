# mqttconnector
Mqtt bridge for piGarden and piGuardian

Mqttconnector allows to transport api of piGarden and piGuardian through mqtt messages to the socket server.

## Official documentation 

Offical documentation of mqttconnector can be found on the [https://www.lejubila.net/2018/11/mqttconnector-ut…ian-tramite-mqtt/](https://www.lejubila.net/2018/11/mqttconnector-ut…ian-tramite-mqtt/)

## License

This script is open-sourced software under GNU GENERAL PUBLIC LICENSE Version 3

## Installation to Raspbian Jessie and Stretch

1) Installs the necessary packages on your terminal:

``` bash
sudo apt-get install python2.7 python-pip
sudo pip install paho-mqtt configparser
```

2) Download and install mqttconnector in your home

``` bash
cd
git clone https://github.com/lejubila/mqttconnector.git
```

3) Install systemd service

``` bash
cd
cp mqttconnector/mqttconnector.service /etc/systemd/system/mqttconnector.service
```

## Configuration

Copy configuration file in /etc

```bash
cd
sudo cp mqttconnector/mqttconnector.ini.sample /etc/mqttconnector.ini
```

Customize the configuration file. 
For more information see [https://www.lejubila.net/2018/11/mqttconnector-ut…ian-tramite-mqtt/](https://www.lejubila.net/2018/11/mqttconnector-ut…ian-tramite-mqtt/)

## Start service and setup autostart at system boot 

For start service use the follow command

``` bash
sudo systemctl start mqttconnector
```

Setup autostart at boot of system with follow command

``` bash
sudo systemctl enable mqttconnector
```



