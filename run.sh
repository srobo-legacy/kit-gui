#!/bin/bash

MYDISP=":3"
Xephyr -screen 480x272 $MYDISP&
sleep 3
URRDISP=$DISPLAY
export DISPLAY="$MYDISP"
matchbox-panel&
matchbox-window-manager -use_titlebar no&
python sroboapplet.py

