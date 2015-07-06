#!/usr/bin/env python

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



# Designed for python 2.7

import Image as image
import sys
import json
from datetime import date
from datetime import timedelta
import datetime
import xml.etree.ElementTree as xet
from xml.dom import minidom


inpLink = sys.argv[1]
outType = sys.argv[2]
outFilePath = sys.argv[3]

blockHeight = 96
sampleRate = 6
sourceTime = int(inpLink[-13:-11])
sourceDateStr = inpLink[-22:-14]

sourceDate = datetime.datetime.strptime(sourceDateStr, '%Y%m%d')

def arrayTo2D(sizex,sizey,array):	# Converts single dimensional array to 2dimensional result with resolution sizex,sizey
	result = []
	for j in range(sizey):
		inner = []
		for i in range(sizex):
			inner.append(array[j*sizex+i])
		result.append(inner)
	
	return result

def arrayFrom2D(sizex,sizey,array):	# Converts 2dimensional array to single dimensional result with resolution sizex,sizey
	result = []
	for j in range(sizey):
		for i in range(sizex):
			result.append(array[j][i])
	
	return result

def timeFromMinutes(mins,sTime):
	mins = mins + sTime*60
	h = (mins / 60) % 24
	m = mins % 60
	if h < 10:
		h = '0'+str(h)
	else:
		h = str(h)
	if m < 10:
		m = '0'+str(m)
	else:
		m = str(m)
	return (h+':'+m)

# short: -6, -4, -2, 0, 2, 3, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 26, 27, 28, 30, 32, 34
# long: 995, 1000, 1005, 1010, 1015, 1020, 1025, 1030
# float: 0.0, 1.0, 2.0, 3.0, 4.0, 5.0
nums = {'-6': [255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 0, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 0, 0, 255],
	'-4': [255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 0, 0, 0, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255],
	'-2': [255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0],
	'0': [255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255],
	'2': [255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0],
	'3': [255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 0, 0, 255],
	'4': [255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255],
	'6': [255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 0, 0, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 0, 0, 255],
	'8': [255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 0, 0, 255],
	'9': [255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 0, 0, 255],
	'10': [255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 0, 0, 255, 255, 255, 0, 255],
	'12': [255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 0, 0, 255, 0, 0, 0, 0],
	'14': [255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 0, 255, 255, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 0, 0, 255, 255, 255, 0, 255],
	'15': [255, 255, 0, 255, 255, 0, 0, 0, 0, 255, 0, 0, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 0, 0, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 0, 0, 0, 255, 255, 0, 0, 255],
	'16': [255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 255, 0, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 0, 0, 0, 255, 255, 0, 0, 255],
	'18': [255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 0, 0, 0, 255, 255, 0, 0, 255],
	'20': [255, 0, 0, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 0, 0, 0, 0, 0, 255, 255, 255, 0, 255],
	'21': [255, 0, 0, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 0, 0, 0, 0, 255, 255, 0, 0, 0],
	'22': [255, 0, 0, 255, 255, 255, 0, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 255, 0, 0, 0, 0],
	'24': [255, 0, 0, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 255, 0, 255, 255, 255, 255, 255, 0, 255, 0, 0, 0, 0, 255, 255, 255, 0, 255],
	'26': [255, 0, 0, 255, 255, 255, 0, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 0, 255, 255, 0, 0, 255],
	'27': [255, 0, 0, 255, 255, 0, 0, 0, 0, 0, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 255, 255, 0, 255, 255],
	'28': [255, 0, 0, 255, 255, 255, 0, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 0, 255, 255, 0, 0, 255],
	'30': [255, 0, 0, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 255, 0, 0, 255, 255, 0, 255, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'32': [255, 0, 0, 255, 255, 255, 0, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 0, 0, 0, 0],
	'34': [255, 0, 0, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 0, 0, 0, 0, 0, 255, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	
	'1030': [255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 255, 0, 0, 0, 0, 255, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'1025': [255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 0, 0, 0, 0, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 0, 0, 0, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 255, 255, 0, 0, 255],
	'1020': [255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 0, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 0, 255, 0, 0, 0, 0, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 255, 255, 255, 0, 255],
	'1015': [255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 0, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 0, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 0, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 255, 255, 0, 0, 0, 0, 255, 255, 255, 0, 255, 255, 255, 0, 0, 0, 255, 255, 0, 0, 255],
	'1010': [255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 0, 0, 0, 255, 255, 255, 0, 255, 255, 255, 0, 0, 0, 255, 255, 255, 0, 255],
	'1005': [255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 0, 0, 0, 0, 0, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 0, 0, 0, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 0, 255, 255, 0, 0, 0, 0, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 0, 255],
	'1000': [255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 0, 0, 0, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255],
	'995': [255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 0, 0, 255, 255, 0, 0, 0, 0, 255, 255, 255, 255, 0, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 0, 255, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 0, 0, 255, 255, 255, 0, 0, 255],
	
	'9.0': [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0],
	'8.0': [255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'7.0': [0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'6.0': [255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'5.0': [0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'4.0': [255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'3.0': [255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 0, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'2.0': [255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 0, 0, 0, 0, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'1.0': [255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 0, 0, 0, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255],
	'0.0': [255, 255, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 255, 255, 0, 255, 0, 255, 0, 255, 0, 255, 255, 0, 0, 255, 255, 255, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 0, 255, 255, 255, 255, 0, 255]
}

output = []




##################################################
# TEMPERATURE EXTRACTION
##################################################

# Image loading
iMin = image.open('temp_min.png').convert('L')
iMax = image.open('temp_max.png').convert('L')
lMin = list(iMin.getdata())
lMax = list(iMax.getdata())

plotRange = {}

# Getting plot range from images
for num in nums:
	if nums[num] == lMin:
		plotRange['min'] = int(num)
	if nums[num] == lMax:
		plotRange['max'] = int(num)

if len(plotRange) != 2:
	print 'FAIL: Unable to recongize temp plot range.'
	sys.exit(1)

plotRange['diff'] = plotRange['max']-plotRange['min']


# Plot image loading
iPlot = image.open('temp_thr.png').convert('L')
lPlot = list(iPlot.getdata())

aPlot = arrayTo2D(iPlot.size[0],iPlot.size[1],lPlot)

# Getting range blocks

if sourceTime == 0:
	blocks = [0,182,364,555]
	blockTimes = [24,24,24]
elif sourceTime == 6:
	blocks = [0,136,319,501,555]
	blockTimes = [18,24,24,6]
elif sourceTime == 12:
	blocks = [0,91,273,456,555]
	blockTimes = [12,24,24,12]
elif sourceTime == 18:
	blocks = [0,54,272,491,555]
	blockTimes = [6,24,24,6]
else:
	sys.exit(1)


# Creating new empty array for corrected plot and reduced line plot
newPlot = []
fPlot = []
for i in range(iPlot.size[1]):
	newPlot.append([])
	fPlot.append([])
	for j in range(iPlot.size[0]):
		newPlot[i].append(255)
		fPlot[i].append(255)



# Curve correction
for col in range(iPlot.size[0]):
	black = []
	for var in range(iPlot.size[1]):
		if aPlot[var][col] == 0:
			black.append(var)
	if len(black) == 0:
		inserted = -1
		added = -1
		continue
	elif len(black) == 1:
		newPlot[black[0]][col] = 0
		added = -1
		inserted = -1
	elif len(black) == 2:
		if abs(black[0]-black[1]) == 2:
			newPlot[black[0]][col] = 0
			newPlot[black[0]+1][col] = 0
			newPlot[black[1]][col] = 0
			added = -1
			inserted = black[0]+1
		else:
			if inserted != -1:
				if inserted == black[0]-1:
					newPlot[black[0]-1][col] = 0
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					added = black[0]-1
					inserted = -1
					continue
				elif inserted == black[1]+1:
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					newPlot[black[1]+1][col] = 0
					added = black[1]+1
					inserted = -1
					continue
			if added != -1:
				if added == black[0]-1:
					newPlot[black[0]-1][col] = 0
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					added = black[0]-1
					inserted = -1
					continue
				elif added == black[1]+1:
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					newPlot[black[1]+1][col] = 0
					added = black[1]+1
					inserted = -1
					continue

			if (aPlot[black[0]-1][col-1] == 255) and (aPlot[black[0]-1][col+1] == 255):
				newPlot[black[0]-1][col] = 0
				newPlot[black[0]][col] = 0
				newPlot[black[1]][col] = 0
				added = black[0]-1
				inserted = -1
				continue
			if (aPlot[black[1]+1][col-1] == 255) and (aPlot[black[0]-1][col+1] == 255):
				newPlot[black[0]][col] = 0
				newPlot[black[1]][col] = 0
				newPlot[black[1]+1][col] = 0
				added = black[1]+1
				inserted = -1
				continue
			added = -1
			inserted = -1
			continue

	elif len(black) > 2:
		if ((black[-1] - black[0])+1) == len(black):
			for b in black:
				newPlot[b][col] = 0
			inserted = -1
			added = -1
		else:
			l = black[0]
			while l <= black[-1]:
				if aPlot[l][col] == 255:
					newPlot[l][col] = 0
					inserted = l
				else:
					newPlot[l][col] = 0
				l += 1
	
newPlotI = image.new(iPlot.mode, iPlot.size)
newPlotI.putdata(arrayFrom2D(iPlot.size[0],iPlot.size[1],newPlot))
newPlotI.save('temp_corrected.png')

# Curve reduction + data extraction
data = {}

outIndex = 0
col = 0
i = 1
for k in range(len(blockTimes)):
	block = blocks[k+1]
	blockTime = blockTimes[k]
	output.append([])
	col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	while col < block:
		black = []
		for var in range(iPlot.size[1]):
			if newPlot[var][col] == 0:
				black.append(var)
		if len(black) == 0:
			midValue = -1
		elif len(black) % 2 == 0:
			midValue = black[(len(black) / 2) + 1]
		
		elif len(black) % 2 != 0:
			midValue = black[int(round(len(black) / 2))]
		if midValue != -1:
			val = ((plotRange['diff'] / float(blockHeight)) * abs(midValue-blockHeight)) + plotRange['min']
			data['time'] = timeFromMinutes(i*10,sourceTime)
			data['temp'] = round(val,3)
			output[outIndex].append({'time': data['time'], 'temp': data['temp']})
		else:
			data['time'] = timeFromMinutes(i*10,sourceTime)
			data['temp'] = 0.0
			output[outIndex].append({'time': data['time'], 'temp': data['temp']})

		i += 1
		col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	outIndex += 1





####################################################
# PRESSURE EXTRACTION
####################################################

# Press Image loading
iMin = image.open('press_min.png').convert('L')
iMax = image.open('press_max.png').convert('L')
lMin = list(iMin.getdata())
lMax = list(iMax.getdata())

plotRange = {}

# Getting plot range from press images
for num in nums:
	if nums[num] == lMin:
		plotRange['min'] = int(num)
	if nums[num] == lMax:
		plotRange['max'] = int(num)

if len(plotRange) != 2:
	print 'FAIL: Unable to recongize pressure plot range.'
	sys.exit(1)

plotRange['diff'] = plotRange['max']-plotRange['min']


# Plot image loading
iPlot = image.open('press_thr.png').convert('L')
lPlot = list(iPlot.getdata())

for i in range(len(lPlot)):
	if lPlot[i] != 255:
		lPlot[i] = 0

aPlot = arrayTo2D(iPlot.size[0],iPlot.size[1],lPlot)


# Creating new empty array for corrected plot and reduced line plot
newPlot = []
fPlot = []
for i in range(iPlot.size[1]):
	newPlot.append([])
	fPlot.append([])
	for j in range(iPlot.size[0]):
		newPlot[i].append(255)
		fPlot[i].append(255)



# Curve correction
for col in range(iPlot.size[0]):
	black = []
	for var in range(iPlot.size[1]):
		if aPlot[var][col] == 0:
			black.append(var)
	if len(black) == 0:
		inserted = -1
		added = -1
		continue
	elif len(black) == 1:
		newPlot[black[0]][col] = 0
		added = -1
		inserted = -1
	elif len(black) == 2:
		if abs(black[0]-black[1]) == 2:
			newPlot[black[0]][col] = 0
			newPlot[black[0]+1][col] = 0
			newPlot[black[1]][col] = 0
			added = -1
			inserted = black[0]+1
		else:
			if inserted != -1:
				if inserted == black[0]-1:
					newPlot[black[0]-1][col] = 0
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					added = black[0]-1
					inserted = -1
					continue
				elif inserted == black[1]+1:
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					newPlot[black[1]+1][col] = 0
					added = black[1]+1
					inserted = -1
					continue
			if added != -1:
				if added == black[0]-1:
					newPlot[black[0]-1][col] = 0
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					added = black[0]-1
					inserted = -1
					continue
				elif added == black[1]+1:
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					newPlot[black[1]+1][col] = 0
					added = black[1]+1
					inserted = -1
					continue

			if (aPlot[black[0]-1][col-1] == 255) and (aPlot[black[0]-1][col+1] == 255):
				newPlot[black[0]-1][col] = 0
				newPlot[black[0]][col] = 0
				newPlot[black[1]][col] = 0
				added = black[0]-1
				inserted = -1
				continue
			if (aPlot[black[1]+1][col-1] == 255) and (aPlot[black[0]-1][col+1] == 255):
				newPlot[black[0]][col] = 0
				newPlot[black[1]][col] = 0
				newPlot[black[1]+1][col] = 0
				added = black[1]+1
				inserted = -1
				continue
			added = -1
			inserted = -1
			continue

	elif len(black) > 2:
		if ((black[-1] - black[0])+1) == len(black):
			for b in black:
				newPlot[b][col] = 0
			inserted = -1
			added = -1
		else:
			l = black[0]
			while l <= black[-1]:
				if aPlot[l][col] == 255:
					newPlot[l][col] = 0
					inserted = l
				else:
					newPlot[l][col] = 0
				l += 1
	
newPlotI = image.new(iPlot.mode, iPlot.size)
newPlotI.putdata(arrayFrom2D(iPlot.size[0],iPlot.size[1],newPlot))
newPlotI.save('press_corrected.png')

# Curve reduction + data extraction
data = {}

outIndex = 0
col = 0
i = 1
for k in range(len(blockTimes)):
	block = blocks[k+1]
	blockTime = blockTimes[k]
	col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	while col < block:
		black = []
		for var in range(iPlot.size[1]):
			if newPlot[var][col] == 0:
				black.append(var)
		if len(black) == 0:
			midValue = -1
		elif len(black) % 2 == 0:
			midValue = black[(len(black) / 2) + 1]
		
		elif len(black) % 2 != 0:
			midValue = black[int(round(len(black) / 2))]
		if midValue != -1:
			val = ((plotRange['diff'] / float(blockHeight)) * abs(midValue-blockHeight)) + plotRange['min']
			data['time'] = timeFromMinutes(i*10,sourceTime)
			data['pressure'] = round(val,3)
			for dic in output[outIndex]:
				if data['time'] == dic['time']:
					dic['pressure'] = data['pressure']

		i += 1
		col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	outIndex += 1




##################################################
# WIND EXTRACTION
##################################################

# Wind Image loading
iMin = image.open('wind_min.png').convert('L')
iMax = image.open('wind_max.png').convert('L')
lMin = list(iMin.getdata())
lMax = list(iMax.getdata())

plotRange = {}

# Getting plot range from wind images
for num in nums:
	if nums[num] == lMin:
		plotRange['min'] = int(num)
	if nums[num] == lMax:
		plotRange['max'] = int(num)

if len(plotRange) != 2:
	print 'FAIL: Unable to recongize wind plot range.'
	sys.exit(1)

plotRange['diff'] = plotRange['max']-plotRange['min']


# Plot image loading
iPlot = image.open('wind.png').convert('L')
lPlot = list(iPlot.getdata())


# Image plot curve extraction (thresholding)
for i in range(len(lPlot)):
	if lPlot[i] != 255:
		if lPlot[i] != 13:
			lPlot[i] = 255
		else:
			lPlot[i] = 0


aPlot = arrayTo2D(iPlot.size[0],iPlot.size[1],lPlot)

# Creating new empty array for corrected plot and reduced line plot
newPlot = []
fPlot = []
for i in range(iPlot.size[1]):
	newPlot.append([])
	fPlot.append([])
	for j in range(iPlot.size[0]):
		newPlot[i].append(255)
		fPlot[i].append(255)



# Curve correction
for col in range(iPlot.size[0]):
	black = []
	for var in range(iPlot.size[1]):
		if aPlot[var][col] == 0:
			black.append(var)
	if len(black) == 0:
		inserted = -1
		added = -1
		continue
	elif len(black) == 1:
		newPlot[black[0]][col] = 0
		added = -1
		inserted = -1
	elif len(black) == 2:
		if abs(black[0]-black[1]) == 2:
			newPlot[black[0]][col] = 0
			newPlot[black[0]+1][col] = 0
			newPlot[black[1]][col] = 0
			added = -1
			inserted = black[0]+1
		else:
			if inserted != -1:
				if inserted == black[0]-1:
					newPlot[black[0]-1][col] = 0
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					added = black[0]-1
					inserted = -1
					continue
				elif inserted == black[1]+1:
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					newPlot[black[1]+1][col] = 0
					added = black[1]+1
					inserted = -1
					continue
			if added != -1:
				if added == black[0]-1:
					newPlot[black[0]-1][col] = 0
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					added = black[0]-1
					inserted = -1
					continue
				elif added == black[1]+1:
					newPlot[black[0]][col] = 0
					newPlot[black[1]][col] = 0
					newPlot[black[1]+1][col] = 0
					added = black[1]+1
					inserted = -1
					continue

			if (aPlot[black[0]-1][col-1] == 255) and (aPlot[black[0]-1][col+1] == 255):
				newPlot[black[0]-1][col] = 0
				newPlot[black[0]][col] = 0
				newPlot[black[1]][col] = 0
				added = black[0]-1
				inserted = -1
				continue
			if (aPlot[black[1]+1][col-1] == 255) and (aPlot[black[0]-1][col+1] == 255):
				newPlot[black[0]][col] = 0
				newPlot[black[1]][col] = 0
				newPlot[black[1]+1][col] = 0
				added = black[1]+1
				inserted = -1
				continue
			added = -1
			inserted = -1
			continue

	elif len(black) > 2:
		if ((black[-1] - black[0])+1) == len(black):
			for b in black:
				newPlot[b][col] = 0
			inserted = -1
			added = -1
		else:
			l = black[0]
			while l <= black[-1]:
				if aPlot[l][col] == 255:
					newPlot[l][col] = 0
					inserted = l
				else:
					newPlot[l][col] = 0
				l += 1
	
newPlotI = image.new(iPlot.mode, iPlot.size)
newPlotI.putdata(arrayFrom2D(iPlot.size[0],iPlot.size[1],newPlot))
newPlotI.save('wind_corrected.png')

# Curve reduction + data extraction
data = {}

outIndex = 0
col = 0
i = 1
for k in range(len(blockTimes)):
	block = blocks[k+1]
	blockTime = blockTimes[k]
	col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	while col < block:
		black = []
		for var in range(iPlot.size[1]):
			if newPlot[var][col] == 0:
				black.append(var)
		if len(black) == 0:
			midValue = -1
		elif len(black) % 2 == 0:
			midValue = black[(len(black) / 2) + 1]
		
		elif len(black) % 2 != 0:
			midValue = black[int(round(len(black) / 2))]
			
		if midValue != -1:
			val = ((plotRange['diff'] / float(blockHeight)) * abs(midValue-blockHeight)) + plotRange['min']
			data['time'] = timeFromMinutes(i*10,sourceTime)
			data['wind'] = round(val,3)
			for dic in output[outIndex]:
				if data['time'] == dic['time']:
					dic['wind'] = data['wind']

		i += 1
		col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	outIndex += 1


#######################################################
# GUSTS EXTRACTION
#######################################################

# Wind Image loading
iMin = image.open('wind_min.png').convert('L')
iMax = image.open('wind_max.png').convert('L')
lMin = list(iMin.getdata())
lMax = list(iMax.getdata())

plotRange = {}

# Getting plot range from wind images
for num in nums:
	if nums[num] == lMin:
		plotRange['min'] = int(num)
	if nums[num] == lMax:
		plotRange['max'] = int(num)

if len(plotRange) != 2:
	print 'FAIL: Unable to recongize gusts plot range.'
	sys.exit(1)

plotRange['diff'] = plotRange['max']-plotRange['min']


# Plot image loading
iPlot = image.open('wind.png').convert('L')
lPlot = list(iPlot.getdata())


# Image plot bars extraction (thresholding)
for i in range(len(lPlot)):
	if lPlot[i] != 255:
		if lPlot[i] != 212:
			lPlot[i] = 255
		else:
			lPlot[i] = 0


aPlot = arrayTo2D(iPlot.size[0],iPlot.size[1],lPlot)


# Creating new empty array for corrected plot and reduced line plot
newPlot = []
fPlot = []
for i in range(iPlot.size[1]):
	newPlot.append([])
	fPlot.append([])
	for j in range(iPlot.size[0]):
		newPlot[i].append(255)
		fPlot[i].append(255)

newPlotI = image.new(iPlot.mode, iPlot.size)
newPlotI.putdata(arrayFrom2D(iPlot.size[0],iPlot.size[1],aPlot))
newPlotI.save('gusts_corrected2.png')

# Bar correction
for col in range(iPlot.size[0]):
	for var in range(iPlot.size[1]):
		if aPlot[var][col] == 0:
			fPlot[var-1][col] = 0
			break

newPlotI = image.new(iPlot.mode, iPlot.size)
newPlotI.putdata(arrayFrom2D(iPlot.size[0],iPlot.size[1],fPlot))
newPlotI.save('gusts_corrected1.png')

for row in range(iPlot.size[1]):
	last = 255
	for var in range(iPlot.size[0]):
		if fPlot[row][var] == 0 and last == 255:
			newPlot[row][var-1] = 0
			newPlot[row][var] = 0
			last = 0
		elif fPlot[row][var] == 0 and last == 0:
			newPlot[row][var] = 0
			last = 0
		elif fPlot[row][var] == 255 and last == 0:
			newPlot[row][var] = 0
			newPlot[row][var+1] = 0
			last = 255
		elif fPlot[row][var] == 255 and last == 255:
			pass

			


newPlotI = image.new(iPlot.mode, iPlot.size)
newPlotI.putdata(arrayFrom2D(iPlot.size[0],iPlot.size[1],newPlot))
newPlotI.save('gusts_corrected.png')

# Data extraction
data = {}

outIndex = 0
col = 0
i = 1
for k in range(len(blockTimes)):
	block = blocks[k+1]
	blockTime = blockTimes[k]
	col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	while col < block:
		barHeight = -1
		for var in range(iPlot.size[1]):
			if newPlot[var][col] == 0:
				barHeight = var
				break
		
		if barHeight != -1:
			val = ((plotRange['diff'] / float(blockHeight)) * abs(barHeight-blockHeight)) + plotRange['min']
		else:
			val = 0
		data['time'] = timeFromMinutes(i*10,sourceTime)
		data['gusts'] = round(val,3)
		for dic in output[outIndex]:
			if data['time'][:2] == dic['time'][:2]:
				dic['gusts'] = data['gusts']

		i += 1
		col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	outIndex += 1




#######################################################
# PRECIPATION RATE EXTRACTION
#######################################################

# Precipation Image loading
iMin = image.open('prec_min.png').convert('L')
iMax = image.open('prec_max.png').convert('L')
lMin = list(iMin.getdata())
lMax = list(iMax.getdata())

plotRange = {}

# Getting plot range from precipation images
for num in nums:
	if nums[num] == lMin:
		plotRange['min'] = int(round(float(num)))
	if nums[num] == lMax:
		plotRange['max'] = int(round(float(num)))

if len(plotRange) != 2:
	print 'FAIL: Unable to recongize precipation plot range.'
	sys.exit(1)

plotRange['diff'] = plotRange['max']-plotRange['min']


# Plot image loading
iPlot = image.open('prec.png').convert('L')
lPlot = list(iPlot.getdata())

# Plot bar extraction (thresholding)
for i in range(len(lPlot)):
	if lPlot[i] != 255:
		if lPlot[i] != 0:
			lPlot[i] = 255

aPlot = arrayTo2D(iPlot.size[0],iPlot.size[1],lPlot)


# Creating new empty array for corrected plot
newPlot = []
fPlot = []
for i in range(iPlot.size[1]):
	newPlot.append([])
	fPlot.append([])
	for j in range(iPlot.size[0]):
		newPlot[i].append(255)
		fPlot[i].append(255)


# Vertical bar correction
for col in range(iPlot.size[0]):
	for var in range(iPlot.size[1]-1):
		if aPlot[var][col] != 0:
			if aPlot[var-1][col] == 0 and aPlot[var+1][col] == 0:
				aPlot[var][col] = 0

# Horizontal bar correction (uncovered bars)
skipList = []
for col in range(iPlot.size[0]-1):
	if col in skipList:
		continue

	for var in range(iPlot.size[1]-1):
		if aPlot[var][col] == 0 and aPlot[var-1][col] != 0:
			if aPlot[var][col+1] != 0 and aPlot[var][col-1] != 0:
				i = 1
				aPlot[var-1][col] = 0
				while aPlot[var][col+i] != 0:
					aPlot[var-1][col+i] = 0
					skipList.append(col+i)
					i += 1
				aPlot[var-1][col+i] = 0
				skipList.append(col+i)

newPlotI = image.new(iPlot.mode, iPlot.size)
newPlotI.putdata(arrayFrom2D(iPlot.size[0],iPlot.size[1],aPlot))
newPlotI.save('prec_corrected.png')

# Bar reduction (top remains)
for col in range(iPlot.size[0]):
	for var in range(iPlot.size[1]):
		if aPlot[var][col] == 0:
			i = 1
			while aPlot[var+i][col] < iPlot.size[1]:
				aPlot[var+i][col] = 255
				i += 1
			break

newPlotI = image.new(iPlot.mode, iPlot.size)
newPlotI.putdata(arrayFrom2D(iPlot.size[0],iPlot.size[1],aPlot))
newPlotI.save('prec_corrected1.png')

# Bar top stretching
skipList = []
for col in range(iPlot.size[0]):
	if col == 0 or col in skipList:
		continue

	for var in range(iPlot.size[1]):
		if aPlot[var][col] == 255 and aPlot[var][col-1] == 0:
			aPlot[var][col] = 0
			skipList.append(col+1)

newPlotI = image.new(iPlot.mode, iPlot.size)
newPlotI.putdata(arrayFrom2D(iPlot.size[0],iPlot.size[1],aPlot))
newPlotI.save('prec_corrected2.png')


# Data extraction
data = {}

outIndex = 0
col = 0
i = 1
for k in range(len(blockTimes)):
	block = blocks[k+1]
	blockTime = blockTimes[k]
	col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	while col < block:
		barHeight = -1
		for var in range(iPlot.size[1]):
			if aPlot[var][col] == 0:
				barHeight = var
				break
		
		if barHeight != -1:
			val = ((plotRange['diff'] / float(blockHeight)) * abs(barHeight-blockHeight)) + plotRange['min']
		else:
			val = 0
		data['time'] = timeFromMinutes(i*10,sourceTime)
		data['precipation_rate'] = round(val,3)
		for dic in output[outIndex]:
			if data['time'][:2] == dic['time'][:2]:
				dic['precipation_rate'] = data['precipation_rate']

		i += 1
		col = int(round((float(block - blocks[k])/(sampleRate * blockTime))*i))
	outIndex += 1






#######################################################
# DATA OUTPUT
#######################################################

outFile = open(outFilePath, 'w')

if outType == 'json':
	for outIndex in range(len(output)):
		dt = (sourceDate + timedelta(days=outIndex)).strftime('%Y-%m-%d')
		for dic in output[outIndex]:
			dic['date'] = dt
			outFile.write(json.dumps(dic) + '\n')

elif outType == 'xml':
	xml = xet.Element('xml', attrib={'version': '1.0'})
	shmu = xet.SubElement(xml, 'SHMU-Aladin', attrib={'date': sourceDateStr, 'time': inpLink[-13:-9]})
	i = 0
	records = []
	temps = []
	press = []
	winds = []
	gusts = []
	precs = []
	for outIndex in range(len(output)):
		dt = (sourceDate + timedelta(days=outIndex)).strftime('%Y-%m-%d')
		for dic in output[outIndex]:
			record = xet.SubElement(shmu, 'record', attrib={'date': dt, 'time': dic['time']})
			records.append(record)
			
			if 'temp' in dic:
				temp = xet.SubElement(records[i], 'temp')
				temp.text = str(dic['temp'])
				temps.append(temp)

			if 'pressure' in dic:
				pres = xet.SubElement(records[i], 'pressure')
				pres.text = str(dic['pressure'])
				press.append(pres)

			if 'wind' in dic:
				wind = xet.SubElement(records[i], 'wind')
				wind.text = str(dic['wind'])
				winds.append(wind)

			if 'gusts' in dic:
				gust = xet.SubElement(records[i], 'gusts')
				gust.text = str(dic['gusts'])
				gusts.append(gust)

			if 'precipation_rate' in dic:
				prec = xet.SubElement(records[i], 'precipation_rate')
				prec.text = str(dic['precipation_rate'])
				precs.append(prec)

			i += 1
	
	outStr = xet.tostring(xml, encoding='utf-8')
	reparsed = minidom.parseString(outStr)
	outFile.write(reparsed.toprettyxml(indent='    '))

outFile.close()

sys.exit(0)
