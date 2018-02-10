#!/usr/bin/python
#coding:utf-8
import urllib2,json
import Stock,Global,CalculationInfo,copy

class CalculateStock(object):
    url = "http://api.finance.ifeng.com/akdaily/?code={0}&type=last"

    def __init__(self,codeList,nameList):
        self.stocks = []
        self.InitData(codeList,nameList)

    def InitData(self,codeList,nameList):
        if len(codeList) != len(nameList):
            print "StockCode != StockName. StockCode count  : {0} StockName count : {1}".format(len(codeList),len(nameList))
            return

        for index, code in enumerate(codeList):
            data = self.CreateStockByCode(code)
            if len(data) > 0:
                stock = Stock.Stock(nameList[index],code,data)
                self.stocks.append(stock)
            else:
                print "there is an error for %s data is empty." % code

    def GetStockCodeTypeStr(self,code):
        code = int(code)
        if code >= 600000:
            return "sh"
        else:
            return "sz"

    def CreateStockByCode(self,code):
        dataFromUrl = []
        if Global.NeedDownloadDataFromUrl:
            dataFromUrl = self.ReadFromUrl(code)
        dataFromLocal = self.ReadFromLocal(code)
        lenUrl = len(dataFromUrl)
        lenLoc = len(dataFromLocal)

        if lenUrl == 0 and lenLoc == 0:
            print "there is no data from both url and local file"
            return []
        elif lenUrl != 0 and lenLoc == 0:
            self.WriteToLocal(dataFromUrl,code)
            return dataFromUrl
        elif lenUrl == 0 and lenLoc != 0:
            return dataFromLocal
        else:
            urlOldestDate = dataFromUrl[0][0]

            if dataFromLocal[0][0] == urlOldestDate:
                self.WriteToLocal(dataFromUrl, code)
                return dataFromUrl
            else:
                for index,value in enumerate(dataFromLocal):
                    if urlOldestDate == value[0]:
                        break
                    else:
                        print "Insert %s data into Url." % value[0]
                        dataFromUrl.insert(index, value)
                self.WriteToLocal(dataFromUrl,code)
                return dataFromUrl

    def WriteToLocal(self,data,code):
        content = json.dumps(data)
        try:
            with open(Global.DataBase + code,'w') as file:
                file.write(content)
            # print "Write File %s Succeed" % code
        except IOError as e:
            print "there is an error when open and write %s" % code
            print e

    def ReadFromUrl(self,code):
        stockCode = self.GetStockCodeTypeStr(code) + code
        stockUrl = self.url.format(stockCode)
        dataFromUrl = []
        try:
            stockRequset = urllib2.Request(stockUrl)
            res_data = urllib2.urlopen(stockRequset)
            res = res_data.read()
            data = json.loads(res)
            if data.has_key("record"):
                dataFromUrl = data["record"]
            else:
                dataFromUrl = []
        except Exception as e:
            print e
        finally:
            pass
        return dataFromUrl

    def ReadFromLocal(self,code):
        try:
            with open(Global.DataBase + code,'r') as file:
                content = json.load(file)
                return content
        except IOError:
            print "There is an error when open and read %s" % code
            return []

    def CalculateAverage(self):
        for index in range(len(self.stocks)):
            value = self.stocks[index]
            today = len(value.datas) - 1
            value.averageInfos = []
            value.averageInfos.append(value.GetMovingAverage(today))
            value.averageInfos.append(value.GetMovingAverage(today - 1))
            value.averageInfos.append(value.GetMovingAverage(today - 2))

    def CalculateMACD(self):
        for index,value in enumerate(self.stocks):
            # print "{0}({1})".format(value.name,value.code)
            today = len(value.datas) - 1
            value.macdInfos = []
            value.macdInfos.append(value.GetMACD(today))
            value.macdInfos.append(value.GetMACD(today - 1))
            value.macdInfos.append(value.GetMACD(today - 2))

    def Calculate(self):
        print "Calculating......"
        self.CalculateAverage()
        self.CalculateMACD()
        count = 0
        for index, value in enumerate(self.stocks):
            resultMACD = value.CheckMACD()
            resultAverage = value.CheckAverage()
            showMACD = resultMACD and resultMACD["Data"]["Show"]
            showAverage = resultAverage and (resultAverage["Data"][20]["Show"] or resultAverage["Data"][30]["Show"] or resultAverage["Data"][60]["Show"])

            if showMACD or showAverage:
                count += 1
                print "================================================\n"
                print "{0}({1}) ".format(value.name,value.code)

            if showMACD:
                print resultMACD["Info"]
                for key in resultMACD["Data"]:
                    print "{0} : {1}".format(key,resultMACD["Data"][key])

            if showAverage:
                print resultAverage["Info"]
                for key in resultAverage["Data"]:
                    print "=====>MA{0}<=====".format(key)
                    dic = resultAverage["Data"][key]
                    for k in dic:
                        print "{0} : {1}".format(k,dic[k])
            if showMACD or showAverage:
                print "\n"
        print "Information Count : %d" % count
            # print "Stock Name : {0}".format(value.name)
            # print "{0}   Today : {1} ".format(value.averageInfos[CalculationInfo.Average.Today].today,
            #                                   value.averageInfos[CalculationInfo.Average.Today].MA5)
            # print "{0}   Yestoday : {1} ".format(value.averageInfos[CalculationInfo.Average.Yestoday].today,
            #                                      value.averageInfos[CalculationInfo.Average.Yestoday].MA5)
            # print "{0}   TheDayBeforeYestoday : {1} ".format(
            #     value.averageInfos[CalculationInfo.Average.TheDayBeforeYestoday].today,
            #     value.averageInfos[CalculationInfo.Average.TheDayBeforeYestoday].MA5)
            # print "==============DIFF==============="
            # print "{0}   Today : {1} ".format(value.macdInfos[CalculationInfo.Average.Today].today,
            #                                   value.macdInfos[CalculationInfo.Average.Today].DIFF)
            # print "{0}   Yestoday : {1} ".format(value.macdInfos[CalculationInfo.Average.Yestoday].today,
            #                                      value.macdInfos[CalculationInfo.Average.Yestoday].DIFF)
            # print "{0}   TheDayBeforeYestoday : {1} ".format(
            #     value.macdInfos[CalculationInfo.Average.TheDayBeforeYestoday].today,
            #     value.macdInfos[CalculationInfo.Average.TheDayBeforeYestoday].DIFF)
            # pass
