#!/bin/sh

COUNTER=1

while [ $COUNTER -lt 255 ]
do
   ping -t 1 192.168.1.$COUNTER 
   COUNTER=$(( $COUNTER + 1 ))
done
