#!/bin/bash

bridge=br0

if [ -n "$1" ]; then
	ip link set $1 up
	sleep 1
	ovs-vsctl add-port $bridge $1
	[ $? -eq 0 ] && exit 0 || exit 1
else
	echo "Error: no port sepcified."
	exit 2
fi
