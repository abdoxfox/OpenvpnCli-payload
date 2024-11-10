#!/bin/bash

python ovpncfg.py  &
sleep 2
read -p "Enter openvpn config path : " configfile

sudo openvpn --config $configfile --http-proxy 127.0.0.1 8889 --connect-retry 2 --connect-retry-max 10


pid=$(sudo netstat -anp | grep 8889| awk '{print$7}'| tr -d "/python" | tail -1)


sudo kill $pid
