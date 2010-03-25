#!/bin/bash

Xephyr -screen 480x272 :3&
sleep 3
URRDISP=$DISPLAY
export DISPLAY=":3"
matchbox-panel&
matchbox-window-manager -use_titlebar no&
python sroboapplet.py

