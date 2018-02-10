#!/usr/bin/python
#coding:utf-8

class StockInfo(object):
    date = ""  # 日期
    open = ""  # 开盘价
    high = ""  # 最高价
    close = ""  # 收盘价
    low = ""  # 最低价
    chg = ""  # 涨跌额
    p_chg = ""  # 涨跌幅
    ma5 = ""  # 5日均价
    ma10 = ""  # 10日均价
    ma20 = ""  # 20日均价
    vma5 = ""  # 5日均量
    vma10 = ""  # 10日均量
    vma20 = ""  # 20日均量
    turnover = ""  # 换手率(指数无此项)

    def __init__(self,list):
        self.date = list[0]
        self.open = list[1]
        self.high = list[2]
        self.close = list[3]
        self.low = list[4]
        self.chg = list[5]
        self.p_chg = list[6]
        self.ma5 = list[7]
        self.ma10 = list[8]
        self.ma20 = list[9]
        self.vma5 = list[10]
        self.vma10 = list[11]
        self.vma20 = list[12]
        self.turnover = list[13]
