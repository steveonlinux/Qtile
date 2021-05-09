#! /bin/bash 
lxsession &
xrandr --output DP-0 --primary --mode 1920x1080 --rate 144.00 --left-of HDMI-0 --output HDMI-0 --mode 1360x768 --rate 59.93 &
picom --experimental-backends --no-fading-openclose &
nitrogen --restore &
urxvtd -q -o -f &
/usr/bin/emacs --daemon &
volumeicon &
nm-applet &
