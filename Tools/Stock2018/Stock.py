#!/usr/bin/python
#coding:utf-8
#coding=utf-8
import urllib,urllib2,json

Url = "http://api.finance.ifeng.com/akdaily/?code={0}&type=last"
MA5 = 0
MA10 = 0
MA20 = 0
MA30 = 0
MA60 = 0
MA120 = 0
MA_Name = ["20日线","30日线","60日线"]
MA_Score = [1,3,5]

StockCode = ["600000","600016","600019","600028","600029","600030","600036","600048","600050","600104","600111","600309","600340","600518","600519","600547","600606","600837","600887","600919","600958","600999","601006","601088","601166","601169","601186","601211","601229","601288","601318","601328","601336","601390","601398","601601","601628","601668","601669","601688","601766","601800","601818","601857","601878","601881","601985","601988","601989","603993","600198","300033","300368","300307","600570","002368","600389","002402","002655","601311","000858","300236","002460","000728","002746","300315","600150","603885","002048","600120","300242","300247","002047","600503","000937","002679","603799","300106","002438","300481","300251","300333","300052"]
StockName = ["浦发银行","民生银行","宝钢股份","中国石化","南方航空","中信证券","招商银行","保利地产","中国联通","上汽集团","北方稀土","万华化学","华夏幸福","康美药业","贵州茅台","山东黄金","绿地控股","海通证券","伊利股份","江苏银行","东方证券","招商证券","大秦铁路","中国神华","兴业银行","北京银行","中国铁建","国泰君安","上海银行","农业银行","中国平安","交通银行","新华保险","中国中铁","工商银行","中国太保","中国人寿","中国建筑","中国电建","华泰证券","中国中车","中国交建","光大银行","中国石油","浙江证券","中国银河","中国核电","中国银行","中国重工","洛阳钼业","大唐电信","同花顺","汇金股份","慈星股份","恒生电子","太极股份","江山股份","和而泰","共达电声","骆驼股份","五粮液","上海新阳","赣锋锂业","国元证券","仙坛股份","掌趣科技","中国船舶","吉祥航空","宁波华翔","浙江东方","明家联合","乐金健康","宝鹰股份","华丽家族","冀中能源","福建金森","华友钴业","西部牧业","江苏神通","濮阳惠成","光线传媒","兆日科技","中青宝"]

def GetStockDataByUrl(url):
	req = urllib2.Request(url)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	data = json.loads(res)
	return data

def GetMovingAverage(data,daybefore):
	if len(data) <= 0:
		return []
	last = len(data) - daybefore
	Sum = 0
	day = 0
	for i in range(last - 120,last)[::-1]:
		Sum +=  float(data[i][3])
		day += 1
		if day == 5:
			MA5 = float("{0:.6}".format(Sum / day))
		elif day == 10:
			MA10 = float("{0:.6}".format(Sum / day))
		elif day == 20:
			MA20 = float("{0:.6}".format(Sum / day))
		elif day == 30:
			MA30 = float("{0:.6}".format(Sum / day))
		elif day == 60:
			MA60 = float("{0:.6}".format(Sum / day))
		elif day == 120:
			MA120 = float("{0:.6}".format(Sum / day))
	return [MA20,MA30,MA60]

def GetAverageResult(data):
	Day0 = GetMovingAverage(data['record'],0)
	Day_1 = GetMovingAverage(data['record'],1)
	if len(Day0) == 0 or len(Day_1) == 0:
		return "Data is None!!!"
	score = 0
	info = ""
	for i in range(0,len(Day0)):
		precent = (Day0[i] - Day_1[i]) / Day_1[i] * 100
		# print "{0}:{1}".format(MA_Name[i],precent)
		if precent > 0.05:
			score += MA_Score[i]
			info += "{0}:{1}  ".format(MA_Name[i],"升")
		elif precent < -0.05:
			score -= MA_Score[i]
			info += "{0}:{1}  ".format(MA_Name[i],"降")
		else:
			info += "{0}:{1}  ".format(MA_Name[i],"平")
	if score <= 0:
		return ""
	return info

def Main():
	if len(StockCode) != len(StockName):
		print "StockCode != StockName. StockCode count  : {0} StockName count : {1}".format(len(StockCode),len(StockName))
		return 
	for index,value in enumerate(StockCode):
		StockInfo = {}
		code = ""
		value_int = int(value)
		if value_int > 600000:
			code = "sh" + value
		else:
			code = "sz" + value
		url = Url.format(code)
		stockData = GetStockDataByUrl(url)
		# print StockName[index] + " : "
		result = GetAverageResult(stockData)
		if result != "":
			print StockName[index] + "(" + value + ") : " + result

Main()