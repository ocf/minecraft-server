#!/bin/sh

mkdir /data/world
mkdir /data/world_nether
mkdir /data/world_the_end

while [ true ]; do
    java -Xms4096M -Xmx4096M -jar paper.jar nogui
    echo Server restarting...
done
