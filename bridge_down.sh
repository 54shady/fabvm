#!/bin/bash

switch=br0

brctl show ${switch} | grep $1 > /dev/null 2>&1
if [ $? -eq 0 ];then
	brctl delif ${switch} $1
fi
ifconfig $1 down
