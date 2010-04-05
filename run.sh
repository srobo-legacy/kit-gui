#!/bin/bash

MYDISP=":3"
Xephyr -screen 480x272 $MYDISP&
sleep 3
DISPLAY="$MYDISP"
matchbox-panel -ns --orientation north&
matchbox-window-manager -use_titlebar no&
python sroboapplet.py

