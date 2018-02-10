#!/usr/bin/python
#coding:utf-8
import StockInfo,CalculationInfo,Global
class Stock(object):
    name = ""
    code = ""
    datas = []
    averageInfos = []
    macdInfos = []
    EMA_Times = 120

    def __init__(self,name,code,data):
        self.name = ""
        self.code = ""
        self.datas = []
        self.averageInfos = []
        self.macdInfos = []
        self.EMA_Times = 120
        self.InitData(name,code,data)


    def InitData(self,name,code,data):
        self.name = name
        self.code = code
        for index,value in enumerate(data):
            self.datas.append(StockInfo.StockInfo(value))

    def GetTheLastInfoDate(self):
        if len(self.datas) <= 0:
            return ""
        info = self.datas[len(self.datas) - 1]
        return info.date

    def GetMovingAverage(self, today):
        if len(self.datas) <= 0:
            return []
        info = CalculationInfo.AverageInfo()
        info.today = self.datas[today].date
        Sum = 0
        day = 0
        for i in range(today - 120, today)[::-1]:
            Sum += float(self.datas[i].close)
            day += 1
            if day == 5:
                info.MA5 = float("{0:.6}".format(Sum / day))
            elif day == 10:
                info.MA10 = float("{0:.6}".format(Sum / day))
            elif day == 20:
                info.MA20 = float("{0:.6}".format(Sum / day))
            elif day == 30:
                info.MA30 = float("{0:.6}".format(Sum / day))
            elif day == 60:
                info.MA60 = float("{0:.6}".format(Sum / day))
            elif day == 120:
                info.MA120 = float("{0:.6}".format(Sum / day))
        return info

    def GetEMA(self, today, days, times):
        if self.EMA_Times < times:
            print "Error : EMA_Times < times"
            return 0
        before = 0
        if times != 0:
            before = self.GetEMA(today, days, times - 1)
        else:
            return 0
        i = today - (self.EMA_Times - times)
        closePrice = float(self.datas[i].close)
        value = closePrice * 2 / float(days) + before * (days - 2) / float(days)
        return value

    def GetDiff(self, today):
        if today >= len(self.datas):
            print "Error : index is too big!!"
            return -1
        # if today < self.EMA_Times:
        #     print "Error : index is too small!! {0}".format(today)
        #     return -1
        ema12 = self.GetEMA(today, 13, self.EMA_Times)
        ema26 = self.GetEMA(today, 27, self.EMA_Times)
        diff = ema12 - ema26
        return diff

    def GetDEA(self, today, days, times):
        before = 0
        if times != 0:
            before = self.GetDEA(today - 1, days, times - 1)
        else:
            return 0
        todayDiff = self.GetDiff(today)
        return todayDiff * 2 / days + before * (days - 2) / days

    def GetMACD(self, today):
        info = CalculationInfo.MACDInfo()
        info.today = self.datas[today].date
        info.DIFF = Global.Float4Down5Up(self.GetDiff(today))
        info.DEA = Global.Float4Down5Up(self.GetDEA(today,10,self.EMA_Times))
        info.MACD = Global.Float4Down5Up((info.DIFF - info.DEA) * 2)
        return info

    def CheckMACD(self):
        result = {}
        if len(self.macdInfos) != 3:
            print "MACD data is Error"
            return {}

        result["Info"] = "MACD数据 Date : {0} ".format(self.macdInfos[Global.Today].today)
        check = {}
        shuoldShow = False
        # if self.macdInfos[Global.Today].DIFF >= self.macdInfos[Global.Today].DEA and self.macdInfos[Global.Yestoday].DIFF <= self.macdInfos[Global.Yestoday].DEA:
        #     check["Cross"] = "MACD日线金叉"
        # elif self.macdInfos[Global.Today].DIFF <= self.macdInfos[Global.Today].DEA and self.macdInfos[Global.Yestoday].DIFF >= self.macdInfos[Global.Yestoday].DEA:
        #     check["Cross"] = "MACD日线死叉"
        # else:
        #     pass

        if self.macdInfos[Global.Today].MACD > self.macdInfos[Global.Yestoday].MACD and self.macdInfos[Global.Yestoday].MACD <= self.macdInfos[Global.TheDayBeforeYestoday].MACD:
            check["Corner"] = "向上拐角"
            shuoldShow = True
        elif self.macdInfos[Global.Today].MACD < self.macdInfos[Global.Yestoday].MACD and self.macdInfos[Global.Yestoday].MACD >= self.macdInfos[Global.TheDayBeforeYestoday].MACD:
            check["Corner"] = "向下拐角"
            shuoldShow = True
        else:
            pass

        # if self.macdInfos[Global.Today].MACD > 0:
        #     check["Color"] = "红"
        # else:
        #     check["Color"] = "绿"
        check["Show"] = shuoldShow
        result["Data"] = check
        return result

    def CompareAverage(self,today,yestoday,before):
        check = {}
        shuoldShow = False
        if today > yestoday:
            # check["Precent"] = "上升阶段 今日斜率 : {0}  昨日斜率 : {1}".format(Global.Float4Down5Up((today - yestoday) / yestoday),Global.Float4Down5Up((yestoday - before) / before))
            # shuoldShow = True
            pass
        elif today < yestoday:
            # check["Precent"] = "下降阶段 今日斜率 : {0}  昨日斜率 : {1}".format(Global.Float4Down5Up((today - yestoday) / yestoday),Global.Float4Down5Up((yestoday - before) / before))
            # shuoldShow = True
            pass
        else:
            # check["Precent"] = "注意持平 昨日斜率 : {0}".format(Global.Float4Down5Up((yestoday - before) / before))
            # shuoldShow = True
            pass
        if today > yestoday and yestoday <= before:
            check["Corner"] = "向上拐角"
            shuoldShow = True
        elif today < yestoday and yestoday >= before:
            check["Corner"] = "向下拐角"
            shuoldShow = True
        else:
            pass

        check["Show"] = shuoldShow
        return check

    def CheckAverage(self):
        result = {}
        if len(self.macdInfos) != 3:
            print "Average data is Error"
            return {}

        result["Info"] = "Average数据 Date : {0} ".format(self.averageInfos[Global.Today].today)
        result["Data"] = {}
        result["Data"][20] = self.CompareAverage(self.averageInfos[Global.Today].MA20,
                                                     self.averageInfos[Global.Yestoday].MA20,
                                                     self.averageInfos[Global.TheDayBeforeYestoday].MA20)
        result["Data"][30] = self.CompareAverage(self.averageInfos[Global.Today].MA30,
                                                     self.averageInfos[Global.Yestoday].MA30,
                                                     self.averageInfos[Global.TheDayBeforeYestoday].MA30)
        result["Data"][60] = self.CompareAverage(self.averageInfos[Global.Today].MA60,
                                                     self.averageInfos[Global.Yestoday].MA60,
                                                     self.averageInfos[Global.TheDayBeforeYestoday].MA60)
        return result