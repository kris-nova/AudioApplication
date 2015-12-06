#!/usr/bin/env bash

###############################################################################
#
# Algorithm [Algorithm.git] Provision Shell Script
#
#				..Kris
###

##
# Update our system first
#
echo '--- Updating ---'
yum -y update
echo '...done'

##
# Define front end dependencies here
# If we are missing a package on the server and it needs to be installed
# It is critical that we also add it here
#
echo '--- Installing dependencies ---'
yum install -y gcc gcc-c++ screen vim nano unzip curl wget man git strace emacs epel-release kernel-devel kernel-headers yasm yasm-devel numpy python-matplotlib
/etc/init.d/vboxadd setup
echo '...done'


##
# Pip and python dependencies here
#
#
yum install -y python-pip python-devel portaudio portaudio-devel
pip install pyaudio
pip install pydub

##
# Download, compile, and install ffmpeg
#
# 
cd /usr/local/src
git clone git://source.ffmpeg.org/ffmpeg.git ffmpeg
cd ffmpeg 
./configure
make
make install

##
# Install gnome
yum -y groupinstall "Desktop" "Desktop Platform" "X Window System" "Fonts"




##
# Lets figure out how you can access this thing
# Spit out some IP addresses to try
#
echo '********************************************************************************'
echo '********************************************************************************'
echo '*'
echo '* You should now be able to find the VM IP address in here :' 
echo '*'
echo '*'
ifconfig | grep "inet"
echo '*'
echo '*'
echo '********************************************************************************'
echo '********************************************************************************'

##
# We should now have an updated and awesome dev server!
#