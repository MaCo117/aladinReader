#!/usr/bin/env bash

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
