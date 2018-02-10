#!/usr/bin/python
#coding:utf-8
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
EMA_Times = 120
Digit = 3

# StockCode = ["600000","600016","600019","600028","600029","600030","600036","600048","600050","600104","600111","600309","600340","600518","600519","600547","600606","600837","600887","600919","600958","600999","601006","601088","601166","601169","601186","601211","601229","601288","601318","601328","601336","601390","601398","601601","601628","601668","601669","601688","601766","601800","601818","601857","601878","601881","601985","601988","601989","603993","600198","300033","300368","300307","600570","002368","600389","002402","002655","601311","000858","300236","002460","000728","002746","300315","600150","603885","002048","600120","300242","300247","002047","600503","000937","002679","603799","300106","002438","300481","300251","300333","300052"]
# StockName = ["浦发银行","民生银行","宝钢股份","中国石化","南方航空","中信证券","招商银行","保利地产","中国联通","上汽集团","北方稀土","万华化学","华夏幸福","康美药业","贵州茅台","山东黄金","绿地控股","海通证券","伊利股份","江苏银行","东方证券","招商证券","大秦铁路","中国神华","兴业银行","北京银行","中国铁建","国泰君安","上海银行","农业银行","中国平安","交通银行","新华保险","中国中铁","工商银行","中国太保","中国人寿","中国建筑","中国电建","华泰证券","中国中车","中国交建","光大银行","中国石油","浙江证券","中国银河","中国核电","中国银行","中国重工","洛阳钼业","大唐电信","同花顺","汇金股份","慈星股份","恒生电子","太极股份","江山股份","和而泰","共达电声","骆驼股份","五粮液","上海新阳","赣锋锂业","国元证券","仙坛股份","掌趣科技","中国船舶","吉祥航空","宁波华翔","浙江东方","明家联合","乐金健康","宝鹰股份","华丽家族","冀中能源","福建金森","华友钴业","西部牧业","江苏神通","濮阳惠成","光线传媒","兆日科技","中青宝"]

# StockCode = ["601766"]
# StockName = ["中车"]

# StockCode = ["600570"]
# StockName = ["恒生"]

# StockCode = ["300251"]
# StockName = ["光纤传媒"]

# StockCode = ["300033"]
# StockName = ["同花顺"]

# StockCode = ["300052"]
# StockName = ["中青宝"]

StockCode = ["002230"]
StockName = ["科大讯飞"]



def GetStockDataByUrl(url):
	req = urllib2.Request(url)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	data = json.loads(res)
	return data

def GetMovingAverage(data,index):
	if len(data) <= 0:
		return []
	Sum = 0
	day = 0
	for i in range(index - 120,index)[::-1]:
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

def GetAverageResult(data,index):
	Day0 = GetMovingAverage(data,index)
	Day_1 = GetMovingAverage(data,index - 1)
	if len(Day0) == 0 or len(Day_1) == 0:
		return "Data is None!!!"
	score = 0
	info = ""
	for i in range(0,len(Day0)):
		precent = (Day0[i] - Day_1[i]) / Day_1[i] * 100
		# print "{0}:{1}".format(MA_Name[i],precent)
		if precent > 0.05:
			# score += MA_Score[i]
			info += "{0}:{1}  ".format(MA_Name[i],"升")
		elif precent < -0.05:
			# score -= MA_Score[i]
			score = -1
			info += "{0}:{1}  ".format(MA_Name[i],"降")
			break
		else:
			info += "{0}:{1}  ".format(MA_Name[i],"平")
	if score < 0:
		return ""
	return info

def GetEMA(data,index,days,times):
	if EMA_Times < times:
		print "Error : EMA_Times < times"
		return 0
	before = 0
	if times != 0:
		before = GetEMA(data,index,days,times - 1)
	i = index - (EMA_Times - times)
	# print data[i][0]
	today = float(data[i][3])
	# print data[index][3]
	value = today * 2 / float(days) + before * (days - 2) / float(days)
	return value

def GetDiff(stockData,index):
	# print "GetDiff : {0}".format(index)
	if index >= len(stockData):
		print "Error : index is too big!!"
		return -1
	if index < EMA_Times:
		print "Error : index is too small!!"
		return -1
	ema12 = GetEMA(stockData,index,13,EMA_Times)
	ema26 = GetEMA(stockData,index,27,EMA_Times)
	diff = ema12 - ema26
	return diff

def GetDEA(data,index,days,times):
	before = 0
	if times != 0:
		# i = index - (EMA_Times - times)
		# print "index : {0}   times{1}".format(index,times)
		before = GetDEA(data,index - 1,days,times - 1)
	# print "today {0}".format(index)
	today = GetDiff(data,index)
	# print today
	return today * 2 / days + before * (days - 2) / days


NEEDBUY = 1
NEEDSELL = -1
NONEED = 0
def CheckIsCorner(stockData,index):
	diff_today = GetDiff(stockData,index)
	diff_yestoday = GetDiff(stockData,index - 1)
	diff_before = GetDiff(stockData,index - 2)
	if diff_before >= diff_yestoday and diff_today > diff_yestoday:
		return [1,(diff_today - diff_yestoday) / diff_yestoday]
	elif diff_before <= diff_yestoday and diff_today < diff_yestoday:
		return [-1,0]
	else:
		return [0,0]

def float4Down5Up(value,digit = Digit):
	return round(value * (10 ** digit)) / (10 ** digit)

def GetMACD(data,today):
	DIFF = float4Down5Up(GetDiff(data,today))
	MACD = float4Down5Up((GetDiff(data,today) - GetDEA(data,today,10,EMA_Times)) * 2)
	DEA = float4Down5Up(GetDEA(data,today,10,EMA_Times)) 
	# print "{0} MACD : {1}    DIFF : {2}    DEA : {3}".format(data[today][0],MACD,DIFF,DEA) 
	return [MACD,DIFF,DEA]
def CheckMACD (data,today):
	result_today = GetMACD (data,today)
	# print "==================="
	result_yestoday = GetMACD (data,today - 1)
	
	# print "==================="
	result_before = GetMACD (data,today - 2)
	# print "==================="

	# if result_today[0] >= 0:
	# 	if result_today[0] <= result_yestoday[0] and result_yestoday[0] > result_before[0]:
	# 		return [NEEDSELL,(result_today[0] - result_yestoday[0]) / result_yestoday[0]]
	# 	else:
	# 		return [NONEED,0]
	# else:
	# 	# print "macd : {0}".format(result_today[0])
	# 	if result_today[0] > result_yestoday[0] and result_yestoday[0] <= result_before[0]:
	# 		return [NEEDBUY,(result_today[0] - result_yestoday[0]) / result_yestoday[0]]
	# 	else:
	# 		return [NONEED,0]
	if result_yestoday[0] != 0:
		if result_today[0] <= result_yestoday[0] and result_yestoday[0] > result_before[0]:
			return [NEEDSELL,(result_today[0] - result_yestoday[0]) / result_yestoday[0]]
		elif result_today[0] > result_yestoday[0] and result_yestoday[0] <= result_before[0]:
			return [NEEDBUY,(result_today[0] - result_yestoday[0]) / result_yestoday[0]]
		else:
			return [NONEED,0]
	else:
		return [NONEED,0]

def Calulation(url,index,code):
	stockData = GetStockDataByUrl(url)["record"]
	print StockName[index] + " : "
	buy = 0
	money = 100000
	today = len(stockData) - 1
	for i in range(today - 200,today):
		result = CheckMACD (stockData,i)
		if result[0] == NEEDBUY:
			aver = GetAverageResult(stockData,today - i)
			if aver != "":
				print "{0}({1}) : {2}".format(StockName[index],code,aver)
				if buy == 0:
					buy = float(stockData[i][3])
					print "{0} NEEDBUY price {1}".format(stockData[i][0],stockData[i][3])
		elif result[0] == NEEDSELL:
			if buy != 0:
				value = (float(stockData[i][3]) - buy) / buy
				money *= (1 + value)
				print "{0} NEEDSELL price {1}  value : {2}% money : {3}".format(stockData[i][0],stockData[i][3],value * 100,money)
				buy = 0
				print "=============================================="
		else:
			if buy != 0:
				 
				if (float(stockData[i][3]) - buy) / buy < -0.03:
					
					value = (float(stockData[i][3]) - buy) / buy
					money *= (1 + value)
					print "{0} NONEED SELL price {1}  value : {2}% money : {3}".format(stockData[i][0],stockData[i][3],value * 100,money)
					print "{0}/{1} = {2}".format(stockData[i][3], buy,(float(stockData[i][3]) - buy) / buy)
					buy = 0
					print "=============================================="

	# end = len(stockData) - 1
	# money = 10000
	# buy = 0
	# for i in range(end - 300,end):
	# 	result = CheckIsCorner(stockData,i)
	# 	if result[0] == NEEDBUY:
	# 		aver = GetAverageResult(stockData,i)
	# 		if aver != "":
	# 			print "{0}({1}) : {2}".format(StockName[index],code,aver)
	# 			buy = float(stockData[i][3])
	# 			print "{0} NEEDBUY price {1}".format(stockData[i][0],stockData[i][3])
	# 	elif result[0] == NEEDSELL:
	# 		if buy != 0:
	# 			value = (float(stockData[i][3]) - buy) / buy
	# 			money *= (1 + value)
	# 			print "{0} NEEDSELL price {1}  value : {2:.2}% money : {3}".format(stockData[i][0],stockData[i][3],value * 100,money)
	# 			buy = 0
	# 	else:
	# 		pass



			# print "NONEED"
	# result = GetAverageResult(stockData)
	# if result != "":
	# 	print StockName[index] + "(" + value + ") : " + result


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
		Calulation(url,index,value)

Main()