#!/usr/bin/env bash
#
# Installation script
#
# SpaceWebRadio
# https://github.com/vektorious/SpaceWebRadio
#
# Copyright (C) 2017-2017 Alexander Kutschera <alexander.kutschera@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

echo "Starting SpaceWebRadio installation" &&
echo "Updating Raspberry Pi..." &&
sudo apt-get update &&
sudo apt-get dist-upgrade &&
echo "MPD" &&
sudo apt-get install mpd mpc alsa-utils &&
sudo apt-get install python-pip &&
sudo apt-get install python-rpi.gpio &&
sudo apt-get install python2.7-dev &&
sudo apt-get install python-pygame &&
sudo apt-get install libimlib2-dev &&
sudo apt-get install librsvg2-dev &&
sudo apt-get install libts-bin &&
sudo apt-get -y purge python-kaa-imlib2 python-kaa-base python-mpd &&
sudo pip install python-mpd2 &&
wget http://archive.raspbian.org/raspbian/pool/main/libs/libsdl1.2/libsdl1.2debian_1.2.15-5_armhf.deb &&
sudo dpkg -i ./libsdl1.2debian_1.2.15-5_armhf.deb &&
sudo apt-mark hold libsdl1.2debian &&
sudo pip install --pre --upgrade kaa-base &&
sudo pip install --pre --upgrade kaa-imlib2 &&
echo "finished installing dependencies" &&
echo "backing up mpd.conf as mpd_backup.conf" &&
sudo mv /etc/mpd.conf /etc/mpd_backup.conf &&
echo "Moving preconfigured mpd.conf into /etc/" &&
sudo cp radio/mpd.conf /etc/mpd.conf &&
echo "Creating Desktop Icon" &&
sudo cp SpaceWebRadio.desktop ~/Desktop/SpaceWebRadio.desktop &&
echo "Loading Playlist" &&
mpc load sender
echo "Done... for now" &&
exit 1
