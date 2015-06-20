# aladinReader

AladinReader is a tool for extracting weather forecast information
from ALADIN graphic meteograms (currently the only public output of
numeric model ALADIN), published by SHMU (Slovak Hydrometeorological Institute).
Main features include:
* Extracts precipation rates, temperature, wind speed, wind gusts
and pressure at resolution of 10 minutes
* Customizable location
* Input either from file, or download from internet
* Two output formats

## Requirements
* [python2.7+](https://www.python.org/download/releases/2.7/)
* [python3.4+](https://www.python.org/download/releases/3.4.0/)
* [imagemagick](http://www.imagemagick.org/script/index.php)

## Installation
None needed.

## Normal usage
To download current meteogram for Horne Srnie location from SHMU website and
start extraction:
```
./aladinReader
```

To specify different location (32173 = Nemsova):
```
./aladinReader -l 32173
```

To specify different output format and filename:
```
./aladinReader -t xml -o myFile.xml
```

For detailed specification of provided options, use:
```
./aladinReader --help
```

## Note
All forecast data are property of Slovak hydrometeorogical institute (SHMU)
and should be used under approval of SHMU. Author takes ABSOLUTELY no
responsibility for improper use of this program.

Data acquired by using this program shall not be considered as accurate or guaranteed and should be handled adequately.

## Credits
aladinReader was written by Marcel Kebisek (maco.kebisek@gmail.com) and is released under GNU GPL License v3.
