#!/usr/bin/env python3

# AladinReader - SHMU Aladin forecast data extractor
# Copyright (C) 2015 Marcel Kebisek
# Contact: marcel.kebisek@gmail.com
#
# This file part of AladinReader.
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


import datetime
from datetime import timedelta
import sys

areaCode = sys.argv[1]


now = datetime.datetime.utcnow()
h = now.strftime('%H')
h = int(h)

if h >= 0 and h < 6:
	print('http://www.shmu.sk/data/datanwp/v2/meteogram/al-meteogram_%s-%s-%s-nwp-.png' % (areaCode, (now - datetime.timedelta(days=1)).strftime('%Y%m%d'), '1800'), end='')
elif h >= 6 and h < 12:
	print('http://www.shmu.sk/data/datanwp/v2/meteogram/al-meteogram_%s-%s-%s-nwp-.png' % (areaCode, now.strftime('%Y%m%d'), '0000'), end='')
elif h >= 12 and h < 17:
	print('http://www.shmu.sk/data/datanwp/v2/meteogram/al-meteogram_%s-%s-%s-nwp-.png' % (areaCode, now.strftime('%Y%m%d'), '0600'), end='')
elif h >= 17 and h <= 23:
	print('http://www.shmu.sk/data/datanwp/v2/meteogram/al-meteogram_%s-%s-%s-nwp-.png' % (areaCode, now.strftime('%Y%m%d'), '1200'), end='')


