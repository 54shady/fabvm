#!/bin/bash

switch=br0

ifconfig $1 up
brctl show ${switch} | grep $1 > /dev/null 2>&1
if [ $? -ne 0 ];then
	brctl addif ${switch} $1
fi
