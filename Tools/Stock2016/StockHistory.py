#!/usr/bin/python
#coding:utf-8

# Step1:通过下面的链接获取数据文件，放入“/Users/Yang/Documents/Job/SelfCodeTool/Stock/HistoryStock/”文件夹中
# 深市数据链接：http://table.finance.yahoo.com/table.csv?s=000001.sz
# 上市数据链接：http://table.finance.yahoo.com/table.csv?s=600000.ss
# Step2:运行本脚本
import urllib2,re,sys,os,pickle,time,shutil,datetime,math
reload(sys)
def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
dirPath = cur_file_dir()
os.chdir(dirPath)
rootDir = os.getcwd()

OutputPath = rootDir + "/Output/"
HistoryStockPath = rootDir + "/HistoryStock/"
ResultOutput = "/Users/Yang/Documents/Self_Examination/大盘预测/StockData/History/"

# if os.path.isdir(OutputPath):
# 	shutil.rmtree(OutputPath)
# os.mkdir(OutputPath)
# os.chdir(OutputPath)

#=====================================================================================================
#从文件中获取数据
HistoryData = {} 
ItemList = ["Date","Open","High","Low","Close","Volume","AdjClose"]
#数据依次是Date,Open,High,Low,Close,Volume,Close
def AnalysisLineData(data):
	datalist = data.split(',')
	LineHistory = {}
	for key,value in enumerate(datalist):
		# print ItemList[key] + "  :  " + value
		if ItemList[key] != "Date":
			value = float(value)
		if ItemList[key] != "":
			LineHistory[ItemList[key]] = value
	return LineHistory



def read(file):
	fileRead = open(file,"r")
	History = {}
	try:
		count = 0
		while True:
			line = fileRead.readline()
			line = line.strip('\n')
			if not line:
				break
			if count != 0:
				History[count-1] = AnalysisLineData(line)
			count += 1 
	finally:
		fileRead.close()
		return History
#=====================================================================================================

#=====================================================================================================
#计算日均线
##计算5、10、20、30、60日均线，其中MA5、MA10、MA20、MA30、MA60是用来计算日线支撑的
def GetMovingAverage(start,dic):
	Sum = 0
	day = 0
	length = len(dic)
	MA5 = 0
	MA10 = 0
	MA20 = 0
	MA30 = 0
	MA60 = 0
	end = start + 60
	if length < start + 60:
		end = length
	for index in range(start,end,1):
		Sum += float(dic[index]["AdjClose"])
		# print Sum
		day += 1
		if day == 5:
			MA5 = float("{0:.5}".format(Sum / day))
		elif day == 10:
			MA10 = float("{0:.5}".format(Sum / day))
		elif day == 20:
			MA20 = float("{0:.5}".format(Sum / day))
		elif day == 30:
			MA30 = float("{0:.5}".format(Sum / day))
		elif day == 60:
			MA60 = float("{0:.5}".format(Sum / day))
			break
	if MA5 == 0:
		MA5 = float("{0:.5}".format(Sum / day))
	if MA10 == 0:
		MA10 = float("{0:.5}".format(Sum / day))
	if MA20 == 0:
		MA20 = float("{0:.5}".format(Sum / day))
	if MA30 == 0:
		MA30 = float("{0:.5}".format(Sum / day))
	if MA60 == 0:
		MA60 = float("{0:.5}".format(Sum / day))	
	return [MA5,MA10,MA20,MA30,MA60]


def CalculateMovingAverage(dic):
	length = len(dic)
	for i in range(0,length):
		array = GetMovingAverage(i,dic)
		dic[i]["MovingAverages"] = array
	return dic


#=====================================================================================================

#=====================================================================================================
#计算增长率
def CalculateIncrease(dic):
	lenght = len(dic)
	for i in range(lenght - 1,-1,-1):
		data = dic[i]
		if i == lenght - 1:
			data["Increase"] = 100
		else:
			dataBefore = dic[i + 1]
			adjClose = float(dataBefore["AdjClose"])
			close = float(data["AdjClose"])
			data["Increase"] = (close - adjClose) / adjClose * 100
			data["Increase"] = float("{0:.3}".format(data["Increase"]))
		dic[i] = data  
	return dic  

#=====================================================================================================

#=====================================================================================================
#分析MACD数据
#按照常规short = 12日EMA,long = 26日EMA,Diff EMA为9日的 
EMA_Diff = 9
EMA_Short = 12
EMA_Long = 26

def GetTodayMACDInfo(data,exinfo):
	info = {}
	percent = float(2) / (EMA_Short + 1)
	info["EMA12"] = float('%0.4f'%(percent * float(data["AdjClose"]) + (1 - percent) * exinfo["EMA12"]))
	percent = float(2) / (EMA_Long + 1)
	info["EMA26"] = float('%0.4f'%(percent * float(data["AdjClose"]) + (1 - percent) * exinfo["EMA26"]))
	info["Diff"] = info["EMA12"] - info["EMA26"]
	percent = float(2) / (EMA_Diff + 1)
	info["DEA"] = float('%0.4f'%(percent * float(exinfo["Diff"]) + (1 - percent) * exinfo["DEA"]))
	info["MACD"] = (info["Diff"] - info["DEA"]) * 2
	return info

def CalculateAllMACD(dic):
	lenght = len(dic)
	for i in range(lenght - 1,-1,-1):
		data = dic[i]
		exinfo = {}
		if i == lenght - 1:
			exinfo["EMA12"] = 0
			exinfo["EMA26"] = 0
			exinfo["Diff"] = 0
			exinfo["DEA"] = 0
		else:
			dataBefore = dic[i + 1]
			exinfo["EMA12"] = dataBefore["EMA12"]
			exinfo["EMA26"] = dataBefore["EMA26"]
			exinfo["Diff"] = dataBefore["Diff"]
			exinfo["DEA"] = dataBefore["DEA"]
		#计算MACD
		info = GetTodayMACDInfo(data,exinfo)
		#写入到数据中
		for index,key in enumerate(info):  
			data[key] = info[key]
		dic[i] = data  
	return dic  
#=====================================================================================================

#=====================================================================================================
##分析KDJ数据
### 计算n日历史最高价
KDJ_N = 9
def Calculate_N_MaxAndMin(data,index):
	Max = float(data[index]["High"])
	Min = float(data[index]["Low"])
	length = len(data)
	end = index + KDJ_N
	if end > length:
		end = length
	for i in range(index,end):
		High = float(data[i]["High"])
		Low = float(data[i]["Low"])
		if High > Max:
			Max = High
		if Low < Min:
			Min = Low
	info = {}
	info["High"] = Max
	info["Low"] = Min
	return info

def GetDayKDJInfoOfIndex(data,index,exinfo):
	percent = float(2)/float(3)
	High_Low = Calculate_N_MaxAndMin(data,index)
	H_N = High_Low["High"]
	L_N = High_Low["Low"]
	C = data[index]["AdjClose"]
	
	if H_N != L_N:
		RSV = float(C - L_N) / float(H_N - L_N) * 100
	else:
		RSV = 0
	K = percent * exinfo["K"] + (1 - percent) * RSV
	D = percent * exinfo["D"] + (1 - percent) * K
	J = 3 * K - 2 * D

	info = {}
	info["K"] = K
	info["D"] = D
	info["J"] = J
	info["RSV"] = RSV
	info["H_" + str(KDJ_N)] = H_N
	info["L_" + str(KDJ_N)] = L_N
	return info


def CalculateAllKDJ(dic):
	length = len(dic)
	for i in range(length - 1,-1,-1):
		exinfo = {}
		if i == length - 1:
			exinfo["K"] = 50
			exinfo["D"] = 50
		else:
			exinfo["K"] = dic[i + 1]["K"]
			exinfo["D"] = dic[i + 1]["D"]
		info = GetDayKDJInfoOfIndex(dic,i,exinfo)
		for index,key in enumerate(info):  
			dic[i][key] = info[key]
	return dic  
#=====================================================================================================

#=====================================================================================================
##计算Boll的数据
## 获得Boll线计算数据
# 同花顺的算法:
# 1）计算MB
# MB = N日内的收盘价之和÷N
# 2）计算标准差MD
# SUM2 = (CLOSE_N - MB)^2 + .......+(CLOSE_1 - MB)^2
# MD= math.sqrt(SUM2/N)
# 3）计算UP、DN线
# UP = MB + 2 × MD
# DN = MB - 2 × MD
# 百度的算法:
# 1）计算MA
# MA = N日内的收盘价之和÷N
# 2）计算标准差MD
# MD = (CLOSE_N - MA)^2 + .......+(CLOSE_1 - MA)^2
# 3）计算MB、UP、DN线
# MB =（N－1）日的MA
# UP = MB + 2 × MD
# DN = MB - 2 × MD
# 这里用的是同花顺的算法
BollDay = 20
MovingAveragesType = 2
def GetBollDataOfIndex(dic,index):
	length = len(dic)
	MB = dic[index]["MovingAverages"][MovingAveragesType]#20日线
	Sum2 = 0
	LastSqr = 0
	for i in range(index,index + BollDay):
		if i < length:
			Close = float(dic[i]["AdjClose"])
			LastSqr = (Close - MB) * (Close - MB)
		Sum2 += LastSqr
	MD = math.sqrt(float(Sum2) / BollDay)
	UP = MB + 2 * MD
	DN = MB - 2 * MD
	info = {}
	info["MB"] = float('%0.2f'%MB)
	info["UP"] = float('%0.2f'%UP)
	info["DN"] = float('%0.2f'%DN)
	return info

def CalculateAllBoll(dic):
	length = len(dic)
	for i in range(length - 1,-1,-1):
		info = GetBollDataOfIndex(dic,i)
		for index,key in enumerate(info):  
			dic[i][key] = info[key]
	return dic  
#=====================================================================================================

#=====================================================================================================
## 计算RSI(相对强弱指标)
RSI6_Day = 6
RSI12_Day = 12
RSI24_Day = 24
def GetRSIOfIndex(dic,index):
	length = len(dic)
	end = index + RSI24_Day
	if end >= length:
		end = length
	day = 0
	RSI6 = 0
	RSI12 = 0
	RSI24 = 0
	Sum_Plus = 0
	Sum_Minus = 0
	Total = 0
	for i in range(index,end):
		day += 1
		CloseNow = float(dic[i]["AdjClose"])
		CloseBef = 0
		if i + 1 < length:
			CloseBef = float(dic[i+1]["AdjClose"])
		Dis = CloseNow - CloseBef

		if Dis > 0:
			Sum_Plus += Dis
		else:
			Sum_Minus += -Dis

		if day == RSI6_Day:
			Total = Sum_Plus + Sum_Minus
			if Total == 0:
				RSI6 = 0
			else:
				RSI6 = Sum_Plus / Total * 100
		elif day ==RSI12_Day:
			Total = Sum_Plus + Sum_Minus
			if Total == 0:
				RSI12 = 0
			else:
				RSI12 = Sum_Plus / Total * 100
		elif day ==RSI24_Day:
			Total = Sum_Plus + Sum_Minus
			if Total == 0:
				RSI24 = 0
			else:
				RSI24 = Sum_Plus / Total * 100
	Total = Sum_Plus + Sum_Minus
	if day < RSI6_Day:
		if Total == 0:
			RSI6 = 0
		else:
			RSI6 = Sum_Plus / (Sum_Plus + Sum_Minus) * 100
		RSI12 = RSI6
		RSI24 = RSI6
	elif day >= RSI6_Day and day < RSI12_Day:
		if Total == 0:
			RSI12 = RSI6
		else:
			RSI12 = Sum_Plus / (Sum_Plus + Sum_Minus) * 100
		RSI24 = RSI12
	elif day >= RSI12_Day and day < RSI24_Day:
		if Total == 0:
			RSI24 = RSI12
		else:
			RSI24 = Sum_Plus / (Sum_Plus + Sum_Minus) * 100
	info = {}
	info["RSI6"] = float('%0.2f'%RSI6)
	info["RSI12"] = float('%0.2f'%RSI12)
	info["RSI24"] = float('%0.2f'%RSI24)
	return info

def CalculateAllRSI(dic):
	length = len(dic)
	for i in range(length - 1,-1,-1):
		info = GetRSIOfIndex(dic,i)
		for index,key in enumerate(info):  
			dic[i][key] = info[key]
	return dic  
#=====================================================================================================

#=====================================================================================================
## 颠倒数据
def disorderData(dic):
	info = {}
	count = 0
	for i in range(len(dic) - 1,-1,-1):
		info[count] = dic[i]
		count += 1
	return info
#=====================================================================================================
#写入到文件
def write(Dic,fileName):
	fileWrite = open(fileName,"w")
	try:
		pickle.dump(Dic, fileWrite)
	finally:
		print "Finish write : " + fileName + "!!!"
		fileWrite.close()
#=====================================================================================================

#=====================================================================================================
#Debug工具函数
def DebugDetail(dic):
	for index,key in enumerate(dic):
		data = dic[key]
		for i,k in enumerate(data):
			if key == len(dic) - 1 or key == len(dic) - 2:
			# if key == 0:
				if k == "Date":
					print data["Date"] + " RSI6 : " + str(data["RSI6"]) + " RSI12 : " + str(data["RSI12"]) + "  RSI24 : " + str(data["RSI24"])

def DebugRangeDetail(dic,index,length):
	sum1 = 0
	sum2 = 0
	up = 0
	dn = 0
	for i in range(index,index + length):
		print "Date : " +str(dic[i]["Date"]) + "   Close : " +str(dic[i]["AdjClose"])
		dis = dic[i]["AdjClose"] - dic[i+1]["AdjClose"]
		print "Dis : " + str(dis)
		if dis > 0:
			sum1 += dis
			up += 1
		elif dis < 0: 
			sum2 += -dis
			dn += 1
	print "up : " +str(up) + "   dn : " +str(dn)
	print "sum1 : " + str(sum1/up) + "  sum2 : " + str(sum2/dn)

#=====================================================================================================
#扫描文件主函数入口
def AnalysisDataMain():
	filelist=os.listdir(HistoryStockPath) 
	# print rootDir
	# print filelist
	for FileName in filelist:
		if FileName != ".DS_Store":
			OutFile = FileName.strip(".csv")
			#1、从文件中读取数据
			Dic = read(HistoryStockPath + FileName) 
			#2、读取的数据进行MACD加工
			Dic = CalculateAllMACD(Dic) ##计算MACD数据
			#3、计算增长率
			Dic = CalculateIncrease(Dic) 
			#4、统计日均线
			Dic = CalculateMovingAverage(Dic)
			#5、统计KDJ数据
			Dic = CalculateAllKDJ(Dic)
			#6、统计Boll数据
			Dic = CalculateAllBoll(Dic)
			#7、统计RSI(相对强弱指数)数据
			Dic = CalculateAllRSI(Dic)
			# if OutFile == "600988":
			# 	DebugRangeDetail(Dic,0,6)
			# 	print GetRSIOfIndex(Dic,0)
			#8、颠倒数据，下标0为最久的数据
			Dic = disorderData(Dic)
			#9、test数据
			# print "\n\n"+OutFile
			# DebugDetail(Dic)

		 	write(Dic,ResultOutput + OutFile)

AnalysisDataMain()

