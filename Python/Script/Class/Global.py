#!/usr/bin/python
#coding:utf-8
RootPath = "/Users/yangyu/Documents/Yangyu/Python/"
ConfigPath = RootPath + 'Script/Config/'
DataBase = ConfigPath + 'DataBase/'
Today = 0
Yestoday = 1
TheDayBeforeYestoday = 2
Digit = 3
NeedDownloadDataFromUrl = True
def Float4Down5Up(value, digit=Digit):
    return round(value * (10 ** digit)) / (10 ** digit)


