#!/usr/bin/env bash

# AladinReader - SHMU Aladin forecast data extractor
# Copyright (C) 2015 Marcel Kebisek
# Contact: marcel.kebisek@gmail.com
#
# This file is part of AladinReader.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# NOTE: 
# All forecast data are property of Slovak hydrometeorogical institute (SHMU)
# and should be used under approval of SHMU. Author takes ABSOLUTELY no
# responsibility for improper use of this program.


RCol='\e[0m'
Red='\e[0;31m'
Gre='\e[0;32m'

# python2.7
dpkg -l | grep -q "python2.7"

if [ $? -eq 0 ]; then
	echo -e "[ ${Gre}OK${RCol} ] Testing dependency python2.7"
else
	echo -e "[ ${Red}FAIL${RCol} ] Testing dependency python2.7"
	echo -e "[ ... ] Attempting to install dependency python2.7"

	apt-get install python2.7

	if [ $? -eq 0 ]; then
		echo -e "[ ${Gre}OK${RCol} ] Attempting to install dependency python2.7"
	else
		echo -e "[ ${Red}FAIL${RCol} ] Attempting to install dependency python2.7"
		echo "Abort."
		exit 1
	fi
fi

# python3
dpkg -l | grep -q "python3.4"

if [ $? -eq 0 ]; then
	echo -e "[ ${Gre}OK${RCol} ] Testing dependency python3.4"
else
	echo -e "[ ${Red}FAIL${RCol} ] Testing dependency python3.4"
	echo -e "[ ... ] Attempting to install dependency python3.4"

	apt-get install python3.4

	if [ $? -eq 0 ]; then
		echo -e "[ ${Gre}OK${RCol} ] Attempting to install dependency python3.4"
	else
		echo -e "[ ${Red}FAIL${RCol} ] Attempting to install dependency python3.4"
		echo "Abort."
		exit 1
	fi
fi

# imagemagick
dpkg -l | grep -q "imagemagick"

if [ $? -eq 0 ]; then
	echo -e "[ ${Gre}OK${RCol} ] Testing dependency imagemagick"
else
	echo -e "[ ${Red}FAIL${RCol} ] Testing dependency imagemagick"
	echo -e "[ ... ] Attempting to install dependency imagemagick"

	apt-get install imagemagick

	if [ $? -eq 0 ]; then
		echo -e "[ ${Gre}OK${RCol} ] Attempting to install dependency imagemagick"
	else
		echo -e "[ ${Red}FAIL${RCol} ] Attempting to install dependency imagemagick"
		echo "Abort."
		exit 1
	fi
fi

echo "Installation successfull."
exit 0
