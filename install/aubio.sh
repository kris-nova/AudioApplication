#!/usr/bin/env bash

###############################################################################
#
# Aubio Library and Python Wrapper Install Script
#
#				..Kris
###

##
# clone the repo
#
yum -y install http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm 
yum install -y waf libsndfile* libsamplerate* jack-audio* libavc* txt2man doxygen ffmpeg ffmpeg-devel

git clone https://github.com/kris-nova/aubio.git
cd aubio
waf configure
waf build
waf install

cd python
python setup.py build
python setup.py install