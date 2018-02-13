# Find the bar!

This application helps for find a Moscow bar by your requirement parameters.

Bars were loaded from [Moscow OpenData Portal](https://apidata.mos.ru)
Here is a [Link](https://data.mos.ru/opendata/7710881420-bary) with bars data.
You need to download an actual ***.json*** version of this file before using this application. 

Fortunately, the Internet connection is not required for application work. 

Application can help you to find the biggest or the smallest bar in Moscow or the closest bar by your actual location.
It prints a name, an address and a capacity of bars.

You can use optional parameter **-b** for finding the biggest bar

You can use optional parameter **-s** for finding the smallest bar

You can use optional parameter **-c -lat \<latitude\> -lon \<longitude\>** for finding the closest bar

# Quickstart
Download the file with bars data:
```
wget https://op.mos.ru/EHDWSREST/catalog/export/get?id=244260 -O ./bars.zip ; unzip ./bars.zip 
```
Example of script launch on Linux, Python 3.*:
```
$ python bars.py ./bars.json -b -s -c -lat 37.2516590 -lon 55.9802988
The biggest bar:
        Bar Name:       Спорт бар «Красная машина»
        Address:        Автозаводская улица, дом 23, строение 1
        SeatsCount:     450
The smallest bar:
        Bar Name:       Сушистор
        Address:        город Москва, Михалковская улица, дом 8
        SeatsCount:     0
The closest bar:
        Bar Name:       САЛЯРИ
        Address:        г. Зеленоград, Сосновая аллея, дом 8
        SeatsCount:     15
```
Get help:
```
$ python bars.py -h
usage: bars.py [-h] [-b] [-s] [-c] [-lat LATITUDE] [-lon LONGITUDE] path

Bars information

positional arguments:
  path                  Path of file with data

optional arguments:
  -h, --help            show this help message and exit
  -b, --big             View information of the biggest bar
  -s, --small           View information of the smallest bar
  -c, --close           View information of the closest bar
  -lat LATITUDE, --latitude LATITUDE
                        Type your actual latitude in DD.DDDDD format for
                        getting the closest bar
  -lon LONGITUDE, --longitude LONGITUDE
                        Type your actual longitude in DD.DDDDD format for
                        getting the closest bar
```

#  Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
