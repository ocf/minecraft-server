#!/bin/sh

mkdir /data/World
mkdir /data/backups

while [ true ]; do
    java -Xms6G -Xmx6G -Dfml.readTimeout=180 @java9args.txt -jar lwjgl3ify-forgePatches.jar nogui
    echo Server restarting...
done
