#!/usr/bin/python
#coding:utf-8
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
if os.path.isdir(OutputPath):
	shutil.rmtree(OutputPath)
os.mkdir(OutputPath)
os.chdir(OutputPath)
# print OutputPath

chooseArray = []
Rank = {}

resultPath = "/Users/Yang/Documents/Self_Examination/大盘预测/2016年09月/"
HistoryPath = "/Users/Yang/Documents/Self_Examination/大盘预测/StockData/History/"


StockCode = ["600198","300033","300368","300307","600570","002368","600389","002402","002655","600547","601311","000858","300236","002460","000728","002746","300315","600150","603885","600120","300242","300247","002047","600503","000937","002679","603799","300106","002438","300481","300251","300333","300052"]#"000538","300093",,"002048"
# StockCode = ["600198"]
# ItemNamelist1 = ["","名字","代码","当前价格","昨收","今开","成交量（手）","外盘","内盘","买一","买一量（手）","买二","买二量（手）","买三","买三量（手）","买四","买四量（手）","买五","买五量（手）","卖一","卖一量（手）","卖二","卖二量（手）","卖三","卖三量（手）","卖四","卖四量（手）","卖五","卖五量（手）","最近逐笔成交","时间","涨跌","涨跌%","最高","最低","价格/成交量（手）/成交额","成交量（手）","成交额（万）","换手率","市盈率","","最高","最低","振幅","流通市值","总市值","市净率","涨停价","跌停价"]
# ItemNamelist2 = ["代码","主力流入","主力流出","主力净流入","主力净流入/资金流入流出总和","散户流入","散户流出","散户净流入","散户净流入/资金流入流出总和","资金流入流出总和1+2+5+6","","","名字","日期"]
ItemNamelist1 = ["","名字","代码","当前价格","昨收","今开","成交量（手）","外盘","内盘","买一","买一量（手）","买二","买二量（手）","买三","买三量（手）","买四","买四量（手）","买五","买五量（手）","卖一","卖一量（手）","卖二","卖二量（手）","卖三","卖三量（手）","卖四","卖四量（手）","卖五","卖五量（手）","最近逐笔成交","时间","涨跌","涨跌%","最高","最低","价格/成交量（手）/成交额","","成交额（万）","换手率","市盈率","","","","振幅","流通市值","总市值","市净率","涨停价","跌停价"]
ItemNamelist2 = ["","主力流入","主力流出","主力净流入","主力净流入/资金流入流出总和","散户流入","散户流出","散户净流入","散户净流入/资金流入流出总和","资金流入流出总和1+2+5+6","","","",""]
Itemlist1 = ["","Name","Code","Now","Last","Start","Volume","Inside","Outside","Buy1","Buy1Vol","Buy2","Buy2Vol","Buy3","Buy3Vol","Buy4","Buy4Vol","Buy5","Buy5Vol","Sell1","Sell1Vol","Sell2","Sell2Vol","Sell3","Sell3Vol","Sell4","Sell4Vol","Sell5","Sell5Vol","TheTradeBefore","Time","Increase","IncreasePercent","Max","Min","Price/Volume/Money","","Money","ExchangePercent","EarningsRatios","","","","Swing","CirculatedMarketValue","TotalValue","BookValue","UpFull","DownFull"]
Itemlist2 = ["","BigFishIn","BigFishOut","BigFishIncrease","BigFishIncreaseInTotal","SmallFishIn","SmallFishOut","SmallFishIncrease","SmallFishIncreaseInTotal","IncreaseInTotal","","","",""]

sys.setdefaultencoding("utf8")
regular_get_data = re.compile(r"\"(.+)\"")
# SinaUrl = "http://hq.sinajs.cn/list="
TencenUrl = "http://qt.gtimg.cn/q="
TencenUrlOther = "http://qt.gtimg.cn/q=ff_"
NowStocksInfo = {}
HistoryInfo = {}
JudgeScore = 0
IsVeto = True
IsShowHowToGetScore = True
Today = time.strftime("%Y-%m-%d",time.localtime(time.time()))
#=====================================================================================================
## 评分系统
def ChangeJudgeScore(change,description):
	global JudgeScore
	# if IsShowHowToGetScore == True:
	# 	print description + " : " + str(change) 
	JudgeScore += change

def TrueVeto(description):
	global IsVeto
	if IsVeto == False:
		if IsShowHowToGetScore == True:
			print description + " : True" 
		IsVeto = True

def ResetJudgeSystem(name):
	if IsShowHowToGetScore == True:
		print "\n=========================>" + name
	global JudgeScore
	JudgeScore = 0
	global IsVeto
	IsVeto = False
#=====================================================================================================

#=====================================================================================================
# 1、获取数据
## 获取现在股票信息
def GetNowStockData():
	total = len(StockCode) * 2
	count = 0
	print "Download StockData : " + str(count) + "/" + str(total),
	sys.stdout.flush()
	for index,value in enumerate(StockCode):
		StockInfo = {}
		code = ""
		value_int = int(value)
		if value_int > 600000:
			code = "sh" + value
		else:
			code = "sz" + value
		url = TencenUrl + code
		# print code + " TencenUrl======>" + url
		content = urllib2.urlopen(url).read().decode("GBK")
		GetNowRealData(content,StockInfo,1)
		count += 1
		print "\rDownload StockData : " + str(count) + "/" + str(total) + "  " + value,
		sys.stdout.flush()

		url = TencenUrlOther + code
		# print "         TencenUrlOther======>" + url
		content = urllib2.urlopen(url).read().decode("GBK")
		GetNowRealData(content,StockInfo,2)
		NowStocksInfo[value_int] = StockInfo
		count += 1
		print "\rDownload StockData : " + str(count) + "/" + str(total) + "  " + value,
		sys.stdout.flush()
	print ""

## 分析当日数据，存入内存待用
def GetNowRealData(string,StockInfo,ItemlistType):
	data = re.findall(regular_get_data,string)
	Itemlist = []
	if ItemlistType == 1:
		Itemlist = Itemlist1
	else:
		Itemlist = Itemlist2
	ItemLen = len(Itemlist)
	RealData = data[0].encode('utf8').split('~')
	for index,value in enumerate(RealData):
		if ItemLen > index:
			if Itemlist[index] != "":
				StockInfo[Itemlist[index]] = value

## 获取历史数据,存入内存待用
def GetHistoryData():
	Files = os.listdir(HistoryPath) 
	for FileName in Files:
		if FileName != ".DS_Store":
			pkl_file = open(HistoryPath + FileName, 'rb')
		 	HistoryInfo[int(FileName)] = pickle.load(pkl_file)
	## 将今日最最基础数据添加进History中 
	ArrangeHistoryToFile()
	## 将计算好的MACD数据计入到History中
	ArrangeMACDHistoryToHistory()
	## 将计算好的日均线计入到History中
	ArrangeMovingAverages()
	## 将计算好的KDJ数据计入到History中
	ArrangeKDJToHistory()
	## 将计算好的Boll数据计入到History中
	ArrangeBollToHistory()
	## 将计算好的RSI数据计入到History中
	ArrangeRSIToHistory()
#=====================================================================================================

#=====================================================================================================
# 2、整理内存数据，计算MACD、均线数据、KDJ的各项指标并且存入内存中待用，最后将数据表写入文件

#----------------------------------------------------
## 将今日最最基础数据添加进History中
# ItemList = ["Date","Open","High","Low","Close","Volume","AdjClose"]
def CheckSameDateData(code):
	HistoryOfCode = HistoryInfo.get(code,-1)
	if HistoryOfCode == -1:
		return -1 #没找到相应股票的数据
	for key,value in enumerate(HistoryOfCode):
		info = HistoryOfCode[value]
		if info["Date"] == Today:
			return value #说明有重复日期的历史数据，返回对应下标
	return -2 #说明没有重复日期的历史数据	

def ArrangeHistoryToFile():
	print "ArrangeHistoryToFile..."
	for k,value in enumerate(StockCode): 
		StockInfo = NowStocksInfo.get(int(value),-1)
		if StockInfo != -1:
			CallBack = CheckSameDateData(int(value))
			if CallBack != -1:
				TodayHistory = {}
				TodayHistory["Date"] = Today
				TodayHistory["Open"] = StockInfo["Start"]
				TodayHistory["High"] = StockInfo["Max"]
				TodayHistory["Low"] = StockInfo["Min"]
				TodayHistory["Close"] = StockInfo["Now"]
				TodayHistory["Volume"] = str(int(StockInfo["Volume"])*100)
				TodayHistory["AdjClose"] = StockInfo["Now"]
				TodayHistory["Increase"] = StockInfo["IncreasePercent"]
				if CallBack == -2:
					HistoryInfo[int(value)][len(HistoryInfo[int(value)])] = TodayHistory
				else:
					HistoryInfo[int(value)][CallBack] = TodayHistory

#----------------------------------------------------
## 计算MACD的数据
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

def ArrangeMACDHistoryToHistory():
	print "ArrangeMACDHistoryToHistory..."
	for _,value in enumerate(StockCode): 
		code = int(value)
		HistoryInCode = HistoryInfo.get(code,-1)
		if HistoryInCode != -1:
			index = len(HistoryInCode) - 1
			data = HistoryInCode[index]
			exinfo = {}
			dataBefore = HistoryInCode[index - 1]
			exinfo["EMA12"] = dataBefore["EMA12"]
			exinfo["EMA26"] = dataBefore["EMA26"]
			exinfo["Diff"] = dataBefore["Diff"]
			exinfo["DEA"] = dataBefore["DEA"]
			info = GetTodayMACDInfo(data,exinfo)
			for _,key in enumerate(info):  
				data[key] = info[key]
			HistoryInfo[code][index] = data

#----------------------------------------------------
##计算如均线
###计算5、10、20、30、60日均线，其中MA5、MA10、MA20、MA30、MA60是用来计算日线支撑的
def GetMovingAverage(code):
	History = HistoryInfo.get(code,-1)
	if History != -1:
		Sum = 0
		day = 0
		length = len(History)
		for key in range(length - 1,-1,-1):
			# print History[key]["Date"]+ "        " + str(History[key]["Close"])
			Sum += float(History[key]["AdjClose"])
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
		return [MA5,MA10,MA20,MA30,MA60]

def ArrangeMovingAverages():
	print "ArrangeMovingAverages..."
	for value in StockCode:
		code = int(value)
		HistoryInCode = HistoryInfo.get(code,-1)
		if HistoryInCode != -1:	
			data = GetMovingAverage(code)
			index = len(HistoryInCode) - 1
			HistoryInfo[code][index]["MovingAverages"] = data



#----------------------------------------------------
##计算KDJ线信息
KDJ_N = 9
def Calculate_N_MaxAndMin(data,index):
	Max = float(data[index]["High"])
	Min = float(data[index]["Low"])
	length = len(data)
	end = index - KDJ_N
	if end < -1:
		end = -1
	for i in range(index,end,-1):
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
	H_N = float(High_Low["High"])
	L_N = float(High_Low["Low"])
	C = float(data[index]["AdjClose"])
	if H_N != L_N:
		RSV = (C - L_N) / (H_N - L_N) * 100
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

##将当天的数据存入历史信息中
def ArrangeKDJToHistory():
	print "ArrangeKDJToHistory..."
	for value in StockCode:
		code = int(value)
		HistoryInCode = HistoryInfo.get(code,-1)
		if HistoryInCode != -1:	
			length = len(HistoryInCode)
			StockLast = HistoryInCode[length - 2]
			exinfo = {}
			exinfo["K"] = StockLast["K"]
			exinfo["D"] = StockLast["D"]
			info = GetDayKDJInfoOfIndex(HistoryInCode,length - 1,exinfo)
			for _,key in enumerate(info):  
				HistoryInCode[length - 1][key] = info[key]
			HistoryInfo[code] = HistoryInCode

#----------------------------------------------------
##计算Boll线信息
### 获得Boll线计算数据
#### 同花顺的算法:
#### 1）计算MB
#### MB = N日内的收盘价之和÷N
#### 2）计算标准差MD
#### SUM2 = (CLOSE_N - MB)^2 + .......+(CLOSE_1 - MB)^2
#### MD= math.sqrt(SUM2/N)
#### 3）计算UP、DN线
#### UP = MB + 2 × MD
#### DN = MB - 2 × MD
#### 百度的算法:
#### 1）计算MA
#### MA = N日内的收盘价之和÷N
#### 2）计算标准差MD
#### MD = (CLOSE_N - MA)^2 + .......+(CLOSE_1 - MA)^2
#### 3）计算MB、UP、DN线
#### MB =（N－1）日的MA
#### UP = MB + 2 × MD
#### DN = MB - 2 × MD
#### 这里用的是同花顺的算法
BollDay = 20
MovingAveragesType = 2
def GetBollData(code):
	HistoryOfCode = HistoryInfo[code]
	length = len(HistoryOfCode)
	MB = HistoryOfCode[length - 1]["MovingAverages"][MovingAveragesType]#20日线
	Sum2 = 0
	for i in range(length - 1,length - 1 - BollDay,-1):
		Close = float(HistoryOfCode[i]["AdjClose"])
		Sum2 += (Close - MB) * (Close - MB)
	MD = math.sqrt(float(Sum2) / BollDay)
	UP = MB + 2 * MD
	DN = MB - 2 * MD
	info = {}
	info["MB"] = float('%0.2f'%MB)
	info["UP"] = float('%0.2f'%UP)
	info["DN"] = float('%0.2f'%DN)
	return info

##将计算的Boll线的数据存入历史信息中
def ArrangeBollToHistory():
	print "ArrangeBollToHistory..."
	for value in StockCode:
		code = int(value)
		HistoryInCode = HistoryInfo.get(code,-1)
		if HistoryInCode != -1:	
			length = len(HistoryInCode)
			info = GetBollData(code)
			for _,key in enumerate(info):  
				HistoryInCode[length - 1][key] = info[key]
			HistoryInfo[code] = HistoryInCode

#----------------------------------------------------
## 计算RSI数据，同花顺上是按照移动平均线计算的，但是我觉得RSI本来就是计算近期
## 多空强弱对比，如果扯上之前的抢入的话，我觉得没必要。
RSI6_Day = 6
RSI12_Day = 12
RSI24_Day = 24
def GetRSIData(dic,index):
	length = len(dic)
	end = index - RSI24_Day
	if end < 0:
		end = -1
	day = 0
	RSI6 = 0
	RSI12 = 0
	RSI24 = 0
	Sum_Plus = 0
	Sum_Minus = 0
	Total = 0
	for i in range(index,end,-1):
		day += 1
		CloseNow = float(dic[i]["AdjClose"])
		CloseBef = 0
		if i - 1 > -1:
			CloseBef = float(dic[i-1]["AdjClose"])
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

def ArrangeRSIToHistory():
	print "ArrangeRSIToHistory..."
	for value in StockCode:
		code = int(value)
		HistoryInCode = HistoryInfo.get(code,-1)
		if HistoryInCode != -1:	
			length = len(HistoryInCode)
			info = GetRSIData(HistoryInCode,length - 1)
			for _,key in enumerate(info):  
				HistoryInCode[length - 1][key] = info[key]
			HistoryInfo[code] = HistoryInCode
#=====================================================================================================

#=====================================================================================================
## 工具
###记录历史数据到文件中
def WriteHistoryToFile():
	for k,value in enumerate(StockCode): 
		HistoryOfCode = HistoryInfo[int(value)]
		fileWrite = open(HistoryPath + value,"w")
		try:
			pickle.dump(HistoryOfCode, fileWrite)
		finally:
			# print "WriteHistoryToFile Finish Write : " + HistoryPath + value + "!!!"
			fileWrite.close()

###将分析信息写入文件
def WriteRecordToFile(writeFileName,str):
	fileWrite = open(writeFileName,"w")
	try:
		fileWrite.write(str)
	finally:
		print "Finish write : " + writeFileName + "!!!"
		fileWrite.close()
#=====================================================================================================

#=====================================================================================================
#逻辑分析区，分析数据内容
#----------------------------------------------------
## 1、主力出入状况
###主力流入流出0.2%一下，主力观察，>0.2%主力流入，<-0.2%主力流出
###统计换手率和主力流入百分率的函数
TestBigFishPercent = 0.3
def CalculateBigFish(code):
	StockInfo = NowStocksInfo[code]
	info = ""
	BigFishIn = float(StockInfo["BigFishIncrease"])/float(StockInfo["TotalValue"]) * 100 / 10000
	if BigFishIn > TestBigFishPercent:
		info = "(1)换手率:{0}% 主力:{1:.3f}%,流入.√".format(StockInfo["ExchangePercent"],BigFishIn)
		ChangeJudgeScore(1,"BigFish主力流入")
	elif BigFishIn < TestBigFishPercent * (-1):
		info = "(1)换手率:{0}% 主力:{1:.3f}%,流出.×".format(StockInfo["ExchangePercent"],BigFishIn)
		ChangeJudgeScore(-1,"BigFish主力流出")
	else:
		info = "(1)换手率:{0}% 主力:{1:.3f}%,观察.".format(StockInfo["ExchangePercent"],BigFishIn)
	return info 

#----------------------------------------------------
## 分析当日股价含义和k先总结
###增/减的绝对值超过5%时为暴涨/暴跌，暴涨记一个×，暴跌记一个√
###统计今日的增长率，最近一段时间的收盘价排名
SuperIncrease = 5 ####暴涨/暴跌SuperIncrease个点的常量定义
TradeDays = 30  ####所谓的最近一段时间内，也就是说TradeDays天（交易天数）
RankPolePercent = 0.1 ####排名在最顶部RankPolePercent为近期高点，反之为近期低点
HammerValue = 4 ####影线超过实体HammerValue倍，才确立
def RankOfRecent(index,dic,During = TradeDays):
	rankAbove = 0
	length = len(dic)
	closePrice = float(dic[index]["AdjClose"])
	# print index,closePrice
	for i in range(length - During,length):
		if i != index:
			# print i,dic[i]["AdjClose"]
			if float(dic[i]["AdjClose"]) >= closePrice:
				rankAbove += 1
	return (rankAbove + 1)

def CalculatePrice(code):
	info = ""
	HistoryInCode = HistoryInfo[code]
	length = len(HistoryInCode)
	NowInfo = HistoryInCode[length - 1]
	IncreaseNow = float(NowInfo["Increase"])
	Open = float(NowInfo["Open"])
	Max = float(NowInfo["High"])
	Min = float(NowInfo["Low"])
	Close = float(NowInfo["AdjClose"])
	MAX_OPEN = Max - Open
	OPEN_MIN = Open - Min
	CLOSE_OPEN = Close - Open
	if CLOSE_OPEN < 0:
		CLOSE_OPEN = -CLOSE_OPEN
	rank = RankOfRecent(length - 1,HistoryInCode)
	rankpercent = float(rank)/float(TradeDays)

	if IncreaseNow > SuperIncrease:
		info = "(2){0}%  排名{1}/{2}".format(IncreaseNow,rank,TradeDays)
	elif IncreaseNow < SuperIncrease * (-1):
		info = "(2){0}%  排名{1}/{2}".format(IncreaseNow,rank,TradeDays)
	else:
		info = "(2){0}%  排名{1}/{2}".format(IncreaseNow,rank,TradeDays)

	isHigh = False
	isLow = False
	if rankpercent < RankPolePercent:
		info += ",近期高位"
		ChangeJudgeScore(-1,"Price近期高位")
		isHigh = True
	elif rankpercent > (1 - RankPolePercent):
		info += ",近期低位"
		ChangeJudgeScore(1,"Price近期低位")
		isLow = True

	isUp = False
	isDown = False
	if CLOSE_OPEN == 0:
		info += ",出现十字星?"
	else:
		if MAX_OPEN / CLOSE_OPEN > HammerValue:
			isUp = True
		if OPEN_MIN / CLOSE_OPEN > HammerValue:
			isDown = True
		if isUp == True and isDown == True:
			info += ",出现十字星?"
		elif isUp == True and isDown == False:
			if isLow == True:
				info += ",并出现锤子，可能止跌√"
				ChangeJudgeScore(3,"Price锤子止跌")
		elif isUp == False and isDown == True:
			if isHigh == True:
				info += ",并出现倒锤子，可能止涨×"
				ChangeJudgeScore(-3,"Price倒锤子止涨")
				TrueVeto("Price倒锤子止涨")
	return info

#----------------------------------------------------
## 分析单日交易是否有跳空信息
def CalculateJump(code):
	info = ""
	HistoryOfCode = HistoryInfo[int(code)]
	length = len(HistoryOfCode)
	StockNow = HistoryOfCode[length - 1]
	StockLast = HistoryOfCode[length - 2]

	lastMax = float(StockLast["High"])
	lastMin = float(StockLast["Low"])
	openPrice = float(StockNow["Open"])
	nowPrice = float(StockNow["AdjClose"])
	Max = float(StockNow["High"])
	Min = float(StockNow["Low"])

	if openPrice < lastMin or openPrice > lastMax:
		if openPrice < lastMin:
			info = "(7)跳空低开,"
			if Max >= lastMin:
				info += "多方回补完全"
				ChangeJudgeScore(1,"Jump多方回补完全")
			elif Max < lastMin and Max > openPrice:
				info += "多方回补但不完全×"
				ChangeJudgeScore(-1,"Jump多方回补不完全")
			else:
				info += "未回补×"
				ChangeJudgeScore(-3,"Jump多方未回补")
		elif openPrice > lastMax:
			info = "(7)跳空高开,"
			if Min <= lastMax:
				info += "空方回补完全"
				ChangeJudgeScore(-1,"Jump空方回补完全")
			elif Min > lastMax and Min < openPrice:
				info += "空方回补但不完全√"
				ChangeJudgeScore(1,"Jump空方回补不完全")
			else:
				info += "未回补√"
				ChangeJudgeScore(3,"Jump空方未回补")
	else:
		info = "(7)无跳空"
	return info

#----------------------------------------------------
## 分析成交量变化信息
### 引起注意的增长量界限
VolumeChangePercent = 40
def CalculateVolume(code):
	info = ""
	HistoryOfCode = HistoryInfo[code]
	length = len(HistoryOfCode)
	StockNow = HistoryOfCode[length - 1]
	StockLast = HistoryOfCode[length - 2]

	VolumeNow = float(StockNow["Volume"])
	VolumeLast = float(StockLast["Volume"])

	if VolumeNow > VolumeLast:
		change = 0
		if VolumeLast == 0:
			pass
		else:
			change = float('%0.1f'%((VolumeNow - VolumeLast)/VolumeLast * 100))
		# print "change : " + change
		info = "(8)成交量" + str(change) + "%"
		if change > VolumeChangePercent:
			info += "√"
			ChangeJudgeScore(1,"Volume放量")
	elif VolumeNow < VolumeLast:
		change = float('%0.1f'%((VolumeNow - VolumeLast)/VolumeLast * 100))
		info = "(8)成交量" + str(change) + "%"
		if change < -VolumeChangePercent:
			info += "×"
			ChangeJudgeScore(-1,"Volume缩量")
	else:
		info = "(8)成交量无变化"
	return info	

#----------------------------------------------------
## 分析KDJ线的信息
K_Score = 10
J_Score = 95
D_Score = 20
J_Day = 5
Dis_Of_KD = 5
def CaculateKDJ(code):
	info = "(4)KDJ日线"
	HistoryOfCode = HistoryInfo.get(code,-1)
	if HistoryOfCode == -1:
		return "(4)MACD无信息"
	length = len(HistoryOfCode)
	StockInfoNow = HistoryOfCode[length - 1]
	StockInfoLast = HistoryOfCode[length - 2]
	K = StockInfoNow["K"]
	D = StockInfoNow["D"]
	J = StockInfoNow["J"]

	K_Last = StockInfoLast["K"]
	D_Last = StockInfoLast["D"]
	J_Last = StockInfoLast["J"]

	content = ""
	isHigh = False
	isLow = False
	if K < K_Score or D < D_Score:
		content = "超卖√"
		isLow = True
		ChangeJudgeScore(3,"KDJ超卖")
	elif K > (100 - K_Score) or D > (100 - D_Score):
		content = "超买x"
		isHigh = True
		ChangeJudgeScore(-3,"KDJ超买")

	temp = ""
	if K_Last < D_Last:
		if K >= D:
			temp = "金叉"
			if isLow == True:
				ChangeJudgeScore(3,"KDJ低位金叉")
			else:
				ChangeJudgeScore(1,"KDJ普通金叉")
		else:
			if D - K < Dis_Of_KD:
				temp = "即将金叉√"
				if isLow == True:
					ChangeJudgeScore(3,"KDJ即将低位金叉")
				else:
					ChangeJudgeScore(1,"KDJ即将普通金叉")
	if K_Last >= D_Last:
		if K <= D:
			temp = "死叉"
			if isHigh == True:
				ChangeJudgeScore(-3,"KDJ高位死叉")
				TrueVeto("KDJ高位死叉")
			else:
				ChangeJudgeScore(-1,"KDJ普通死叉")
		else:
			if K - D < Dis_Of_KD:
				temp = "即将死叉x"
				if isHigh == True:
					ChangeJudgeScore(-3,"KDJ即将高位死叉")
					TrueVeto("KDJ即将高位死叉")
				else:
					ChangeJudgeScore(-1,"KDJ即将普通死叉")
	if content != "":
		if temp != "":
			content = "," + temp
	else:
		content = temp

	# if J < J_Last and K <= D:
		# TrueVeto("KDJ死叉后下降过程中")

	Days = 0 
	for i in range(1,J_Day + 1):
		if HistoryOfCode[length - i]["J"] > J_Score:
			# print str(code) + "=======>" + str(i) + "  : " + str(HistoryOfCode[length - i]["J"]) 
			Days += 1
	if Days == J_Day:
		temp = "形成短期顶部x"
		ChangeJudgeScore(-5,"KDJ短期顶部")
		TrueVeto("J线5日100行程KDJ短期顶部")
	if Days == -J_Day:
		temp = "形成短期底部√"
		ChangeJudgeScore(5,"KDJ短期底部")
	if content != "":
		if temp != "":
			content = "," + temp
	else:
		content = temp
	info += content
	if content == "":
		info += "今日无需关注"
	return info

#----------------------------------------------------
## 分析MACD线的信息  
MACDWaringLimit = 0.4  ####MACD线翻红之前的预警界限
def CaculateMACD(code):
	info = "(4)MACD日线"
	HistoryOfCode = HistoryInfo.get(code,-1)
	if HistoryOfCode == -1:
		return "(4)MACD无信息"
	length = len(HistoryOfCode)
	MACD_T = HistoryOfCode[length - 1]["MACD"]#MACD_Today
	MACD_Y = HistoryOfCode[length - 2]["MACD"]#MACD_Yestoday
	MACD_B = HistoryOfCode[length - 3]["MACD"]#MACD_BeforeYestoday
	# print "MACD_Today : "  + str(MACD_Today)
	# print "MACD_Yestoday : "  + str(MACD_Yestoday)
	# print "MACD_BeforeYestoday : "  + str(MACD_BeforeYestoday)

	if MACD_T > MACD_Y:
		if MACD_Y > 0:
			info += "红线加长" 
			ChangeJudgeScore(3,"MACD红线加长")
		elif MACD_T < 0:
			info += "绿线缩短"
			if MACD_T > -MACDWaringLimit:
				info += ",即将翻红√"
				ChangeJudgeScore(5,"MACD即将翻红")
			else:
				ChangeJudgeScore(1,"MACD绿线缩短")
		else:
			info += "绿线翻红"
			ChangeJudgeScore(3,"MACD绿线翻红")
	elif MACD_T < MACD_Y:
		TrueVeto("MACD下降")
		if MACD_T > 0:
			info += "红线缩短"
			if MACD_T < MACDWaringLimit:
				info += ",即将翻绿×"
				ChangeJudgeScore(-5,"MACD即将翻绿")
			else:
				ChangeJudgeScore(-1,"MACD红线缩短")
		elif MACD_Y < 0:
			info += "绿线加长" 
			ChangeJudgeScore(-3,"MACD绿线加长")
		else:
			info += "红线翻绿"
			ChangeJudgeScore(-3,"MACD红线翻绿")
	else:
		info += "无变化"

	if MACD_T > MACD_Y and MACD_Y > MACD_B:
		if (MACD_T - MACD_Y) > (MACD_Y - MACD_B):
			info += ",增速加快"
			ChangeJudgeScore(1,"MACD增速加快")
		elif (MACD_T - MACD_Y) < (MACD_Y - MACD_B):
			info += ",增速减缓"
		else:
			info += "增速不变"
	elif MACD_T < MACD_Y and MACD_Y > MACD_B:
		info += ",顶拐角出现"
		ChangeJudgeScore(-3,"MACD顶拐角出现")
	elif MACD_T > MACD_Y and MACD_Y < MACD_B:
		info += ",底拐角出现"
		ChangeJudgeScore(3,"MACD底拐角出现")
	elif MACD_T < MACD_Y and MACD_Y < MACD_B:
		if (MACD_Y - MACD_T) > (MACD_B - MACD_Y):
			info += ",减速加快"
			ChangeJudgeScore(-1,"MACD减速加快")
		elif (MACD_Y - MACD_T) < (MACD_B - MACD_Y):
			info += ",减速减缓"
		else:
			info += ",减速不变"
	else:
		print "不会有这种可能的！！！"
	return info

#----------------------------------------------------
## 分析RSI线的信息  
RSIWaringLine = 15
RSITurnLine = 50
RSICrossLine = 30  
def CaculateRSI(code):
	info = "(5)RSI日线"
	HistoryOfCode = HistoryInfo[code]
	length = len(HistoryOfCode)
	StockNow = HistoryOfCode[length - 1]
	RSI6_Now = StockNow["RSI6"]
	RSI12_Now = StockNow["RSI12"]
	StockBef = HistoryOfCode[length - 2]
	RSI6_Bef = StockBef["RSI6"]
	RSI12_Bef = StockBef["RSI12"]

	if RSI6_Now >= (1 - RSIWaringLine):
		info += "短期超买."
		ChangeJudgeScore(-3,"RSI短期超买")
	elif RSI6_Now < (1 - RSIWaringLine) and RSI6_Now >= RSITurnLine:
		info += "多方市场."
		ChangeJudgeScore(1,"RSI多方市场")
	elif RSI6_Now < RSITurnLine and RSI6_Now > RSIWaringLine:
		info += "空方市场."
		ChangeJudgeScore(-1,"RSI空方市场")
	else:
		info += "短期超卖."
		ChangeJudgeScore(3,"RSI短期超卖")

	return info

#----------------------------------------------------
## 分析Boll通道信息  
PassChangeLimit = 0.1
def CaculateBoll(code):
	info = "(6)Boll通道信息未开通"
	HistoryOfCode = HistoryInfo[code]
	length = len(HistoryOfCode)
	StockInfo = HistoryOfCode[length - 1]
	StockInfoBf = HistoryOfCode[length - 2]
	Close = float(StockInfo["AdjClose"]) 
	MB = float(StockInfo["MB"])
	UP = float(StockInfo["UP"])
	DN = float(StockInfo["DN"])
	Close_Bf = float(StockInfoBf["AdjClose"])
	MB_Bf = float(StockInfoBf["MB"])
	UP_Bf = float(StockInfoBf["UP"])
	DN_Bf = float(StockInfoBf["DN"])
	DisNow = UP - DN
	DisBef = UP_Bf - DN_Bf
	PassChange = DisNow - DisBef

	percent = (Close - DN) / Close
	if((Close - DN) / Close < 0.05):
		print "percent===========================>" + str(percent)
		# print "UP===========================>" + str(UP)
		# print "NOW===========================>" + str(Close)
		# print "DN===========================>" + str(DN)
	if Close >= Close_Bf:
		if Close >= UP:
			info = "(6)Boll通道突破上沿,卖点信号x"
			ChangeJudgeScore(-5,"Boll卖点信号")
			TrueVeto("Boll卖点")
		else:
			if Close > MB:
				if MB >= Close_Bf:
					info = "(6)Boll通道向上突破中线,加码信号"
					ChangeJudgeScore(1,"Boll加码信号")
				else:
					TrueVeto("Boll在MD上方")
			else:
				info = "(6)Boll通道无操作"
	else:
		if Close <= DN:
			info = "(6)Boll通道突破下沿,买点信号√"
			ChangeJudgeScore(5,"Boll买点信号")
		else:
			if Close <= MB:
				if MB < Close_Bf:
					info = "(6)Boll通道向下突破中线,减码信号"
					ChangeJudgeScore(-1,"Boll减码信号")
			else:
				info = "(6)Boll通道无操作"
				TrueVeto("Boll在MD上方")

	if MB >= MB_Bf:
		info += ",下降通道"
		ChangeJudgeScore(-1,"Boll下降通道")
	else:
		info += ",上升通道"
		ChangeJudgeScore(1,"Boll上升通道")

	if PassChange <= PassChangeLimit and PassChange >= -PassChangeLimit:
		info += ",保持之前趋势."
	elif PassChange < -PassChangeLimit:
		info += ",通道收窄."
		ChangeJudgeScore(-1,"Boll趋于震荡")
	else:
		info += ",通道扩张."
		ChangeJudgeScore(1,"Boll趋于机会")
	return info
#----------------------------------------------------
## 计算日均线信息
###规定比压力日线多LimitPercent以上算突破，比压力线少LimitPercent以内算压制成功，
###比如LimitPercent为0.5%，压力线30点，收盘价超过30.15点算突破，反之压制成功
###支撑日线同理
LimitPercent = 0.003 ####界线百分率
#未受到支撑或压迫返回0，突破支撑返回-2，受到支撑返回-1，突破压迫返回+2,受到压迫返回+1
def CalCulateALine(LineName,Line,code):
	length = len(HistoryInfo[code])
	StockInfo = HistoryInfo[code][length - 1]

	Open = float(StockInfo["Open"])
	Close = float(StockInfo["AdjClose"])
	Max = float(StockInfo["High"])
	Min = float(StockInfo["Low"])

	LimitBelow = Line * (1 - LimitPercent)
	LimitUp = Line * (1 + LimitPercent)
	# print "\n\n" + StockInfo["Name"] + "  " + LineName + "=====================>"
	# print "Line" + str(Line)
	# print "LimitUp" + str(LimitUp)
	# print "LimitBelow" + str(LimitBelow)
	# print "openPrice" + str(openPrice)
	# print "nowPrice" + str(nowPrice)
	# print "Max" + str(Max)
	# print "Min" + str(Min)
	if Open >= Line:
		if Close >= Line:
			if Min > LimitUp:
				# print "未受到" + str(LineName) + "日线支撑"
				return 0
			else:
				# print "受到" + str(LineName) + "日线支撑"
				ChangeJudgeScore(1,"MovingAverage" + "受到" + str(LineName) + "日线支撑")
				return -1
		else:
			# print "突破" + str(LineName) + "日线支撑"
			ChangeJudgeScore(-1,"MovingAverage" + "突破" + str(LineName) + "日线支撑")
			return -2
	else:
		if Close < Line:
			if Max < LimitBelow:
				# print "未受到" + str(LineName) + "日线压迫"
				return 0
			else:
				# print "受到" + str(LineName) + "日线压迫"
				ChangeJudgeScore(-1,"MovingAverage" + "受到" + str(LineName) + "日线压迫")
				return 1
		else:
			# print "突破" + str(LineName) + "日线压迫"
			ChangeJudgeScore(1,"MovingAverage" + "突破" + str(LineName) + "日线压迫")
			return 2

###CalCulateALine返回值+2就是存储字符串，即0~4依次是支撑，突破支撑，不相关，压迫，突破压迫
def CalculateMovingAverage(code):
	MANameList = [5,10,20,30,60]
	length = len(HistoryInfo[code])
	MAList = HistoryInfo[code][length - 1]["MovingAverages"]
	info = ""
	dic = {}
	ResultList = ["","","","",""]
	index = 0

	for MA in MAList:
		Name = str(MANameList[index])
		result = CalCulateALine(Name,MA,code) + 2
		index += 1
		if ResultList[result] == "":
			ResultList[result] += Name
		else:
			ResultList[result] += "," + Name
	if ResultList[0] != "":
		info += "突破" + ResultList[0] + "日线支撑×"
	if ResultList[1] != "":
		if info != "":
			info += ","
		info += "受到" + ResultList[1] + "日线支撑√"
	if ResultList[3] != "":
		if info != "":
			info += ","
		info += "受到" + ResultList[3] + "日线压迫×"
	if ResultList[4] != "":
		if info != "":
			info += ","
		info += "突破" + ResultList[4] + "日线压迫√"
	if info == "":
		info = "无日线变化"
	info = "(9)" + info  + "."
	return info
#=====================================================================================================

#=====================================================================================================
#入口函数
##计算信息
## 分析结果

def AnalysisResult(name):
	Space_Count = 10
	info = name
	count = 0
	if IsVeto == True:
		info += "禁止买入\n"
		count = 35
	else:
		info += "得分 : " + str(JudgeScore) + "\n"
		count = Space_Count - JudgeScore * 2
	for i in range(count):
		info = "    " + info
	return info 
## 初始化评判分数
# ["BigFish"] = 1
# ["Price"] = 4
# ["KDJ"] = 20
# ["MACD"] = 20
# ["RSI"] = 10
# ["Boll"] = 20
# ["Jump"] = 10
# ["Volume"] = 5
# ["MovingAverage"] = 10

def sort(array,isAscent):
	length = len(array)
	i = 0 
	while( i < length - 1):
		k = i + 1
		while(k < length):
			if(isAscent):
				if(array[i]["Rank"] > array[k]["Rank"]):
					tmp = array[i]
					array[i] = array[k]
					array[k] = tmp
			else:
				if(array[i]["Rank"] < array[k]["Rank"]):
					tmp = array[i]
					array[i] = array[k]
					array[k] = tmp
			k += 1
		i += 1
	return array

# array[i][code] = Rank(30 Day's Rank)
def Order():
	array_price_30 = []
	array_price_100 = []
	array_bollDown = []
	array_price_now = []
	# print NowStocksInfo
	for key,code in enumerate(NowStocksInfo):
		HistoryOfCode = HistoryInfo[code]
		# create price array 
		rank = RankOfRecent(len(HistoryOfCode) - 1, HistoryOfCode)
		if(rank > 20):
			array_price_30.append({"Code" : code, "Rank" : rank, "Number" : str(NowStocksInfo[code]['Code'])})

		rank_100 = RankOfRecent(len(HistoryOfCode) - 1, HistoryOfCode,100)
		if(rank_100 > 80):
			array_price_100.append({"Code" : code, "Rank" : rank_100, "Number" : str(NowStocksInfo[code]['Code'])})

		length = len(HistoryOfCode)
		NowInfo = HistoryOfCode[length - 1]
		IncreaseNow = float(NowInfo["Increase"])
		array_price_now.append({"Code" : code, "Rank" : IncreaseNow, "Number" : str(NowStocksInfo[code]['Code'])})

		#create boll down array
		
		StockInfo = HistoryOfCode[length - 1]
		Close = float(StockInfo["AdjClose"]) 
		MB = float(StockInfo["MB"])
		UP = float(StockInfo["UP"])
		DN = float(StockInfo["DN"])
		LastClose = float(HistoryOfCode[length - 2]["AdjClose"])
		ToBottomPercent = float("{0:.4}".format((LastClose - DN) / LastClose))
		percent = float("{0:.4}".format(ToBottomPercent * 100 + IncreaseNow))
		if(percent < 1):
			temp = "Today open : {0}%     Now : {1}%".format(ToBottomPercent * 100,IncreaseNow)
			array_bollDown.append({"Code" : code, "Rank" : percent, "Number" : str(NowStocksInfo[code]['Code']), "Description" : temp})



	Rank["Price_100"] = sort(array_price_100, False)
	Rank["Price_30"] = sort(array_price_30, False)
	Rank["Rank_BollDown"] = sort(array_bollDown, True)
	Rank["Price"] = sort(array_price_now, True)

	# print Rank["PricesSort_Rank"]
	# endlist = []
	# for _,value in enumerate(Rank):
	# 	print value
	# 	tmp = []
	# 	for _,k in enumerate(Rank[value]):
	# 		if len(endlist) ==0 or k['Code'] in endlist:
	# 			tmp.append(k['Code'])
	# 		print "{0}({1}) : {2}".format(NowStocksInfo[k['Code']]["Name"],k["Number"],k['Rank'])
	# 	endlist = tmp 
	# 	print "\n"
	# print "Fit your choose : "
	# for index,value in enumerate(endlist):
	# 	print value 
	# 	print "{0}({1})".format(NowStocksInfo[value]["Name"],value)

def OrderBollDown():
	pass

def CalculateInfo():
	info = "\n\n"
	outputScreen = "\n\n"
	result = ""
	global IsShowHowToGetScore
	IsShowHowToGetScore = True
	for key,value in enumerate(NowStocksInfo):

		ResetJudgeSystem(NowStocksInfo[value]["Name"])
		string = ""
		info += NowStocksInfo[value]["Name"] + ":"
		outputScreen += NowStocksInfo[value]["Name"] + ":"
		string = CalculateBigFish(value)   	  		#(1)统计主力流入情况		√
		info += string
		if(isGet(str(1)) or isGet(str(0))):
			outputScreen += string
	 	string = CalculatePrice(value)		  		#(2)统计价格				√
	 	info += string
		if(isGet(str(2)) or isGet(str(0)) or isGet(str(10))):
			outputScreen += string
		string = CaculateKDJ(value)		  	  		#(3)统计JDK				√
		info += string
		if(isGet(str(3)) or isGet(str(0))):
			outputScreen += string
		string = CaculateMACD(value)		  	  		#(4)统计MACD日线			√
		info += string
		if(isGet(str(4)) or isGet(str(0))):
			outputScreen += string
		string = CaculateRSI(value)			  		#(5)统计RSI				√
		info += string
		if(isGet(str(5)) or isGet(str(0))):
			outputScreen += string
		string = CaculateBoll(value)			  		#(6)统计Boll通道			√
		info += string
		if(isGet(str(6)) or isGet(str(0)) or isGet(str(10))):
			outputScreen += string	
		string = CalculateJump(value)			  	#(7)统计跳空				√
		info += string
		if(isGet(str(7)) or isGet(str(0))):
			outputScreen += string
		string = CalculateVolume(value)		  		#(8)成交量对比			√
		info += string
		if(isGet(str(8)) or isGet(str(0))):
			outputScreen += string
		string = CalculateMovingAverage(value)  		#(9)日线支撑压迫			√
		info += string
		if(isGet(str(9)) or isGet(str(0))):
			outputScreen += string
		string = "\n\n"
		info += string
		outputScreen += string
		result += AnalysisResult(NowStocksInfo[value]["Name"])
	info += result
	outputScreen += result
	print outputScreen
	WriteRecordToFile(resultPath + Today + ".txt",info)

##整理数据
def ArrageData():
	#获取数据
	GetNowStockData()
	#获取历史数
	GetHistoryData()
	#将最新的历史数据写入文件
	# WriteHistoryToFile()

#=====================================================================================================

# def isGet(char):
# 	for index,value in enumerate(chooseArray):
# 		if(cmp(value,char) == 0):
# 			return True
# 	return False



# 整理数据
ArrageData()
# 计算需要的结果
# CalculateInfo()

#获得支持的排序
Order()
# lista = []

# lista.append("a")
# lista.append("b")
# lista.append("c")
# lista.append("d")
# lista.append("e")
# print lista

# lista.remove("b")
# print lista

RecordList = []
while(True):
	print("\n\nWhat do you want to Rank?\n(1).30 Days Price Rank\n(2).Boll DownLine\n(3).Print Totally\n(4).Start over again\n(5).100 Days Price Rank\n(6).Price Rank\n(0).Quit")
	choice = raw_input("Press your choice : ")
	os.system("clear")
	temp = []
	if(cmp(choice,"0") == 0):
		break
	elif(cmp(choice,"1") == 0):
		for _,k in enumerate(Rank["Price_30"]):
			temp.append(k['Code'])
			print "{0}({1}) : {2}/30".format(NowStocksInfo[k['Code']]["Name"],k["Number"],k['Rank'])
	elif(cmp(choice,"5") == 0):
		for _,k in enumerate(Rank["Price_100"]):
			temp.append(k['Code'])
			print "{0}({1}) : {2}/100".format(NowStocksInfo[k['Code']]["Name"],k["Number"],k['Rank'])
	elif(cmp(choice,"2") == 0):
		for _,k in enumerate(Rank["Rank_BollDown"]):
			temp.append(k['Code'])
			print "{0}({1}) : {2}%=========>{3}".format(NowStocksInfo[k['Code']]["Name"],k["Number"],k['Rank'],k['Description'])
	elif(cmp(choice,"6") == 0):
		for _,k in enumerate(Rank["Price"]):
			temp.append(k['Code'])
			print "{0}({1}) : {2}".format(NowStocksInfo[k['Code']]["Name"],k["Number"],k['Rank'])
	elif(cmp(choice,"4") == 0):
		ArrageData()
		Order()
		RecordList = []
		continue
	elif(cmp(choice,"3") == 0):
		for index,value in enumerate(RecordList):
			print "{0}".format(NowStocksInfo[value]["Name"])
		continue
	else:
		break


	if len(RecordList) == 0:
		RecordList = temp
	else:
		index = len(RecordList)-1
		while(index >= 0):
			value = RecordList[index]
			if value not in temp:
				RecordList.remove(value)
			index -= 1;
