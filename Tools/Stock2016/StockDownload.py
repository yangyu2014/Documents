import urllib,time,os,shutil
StockCode = ["600198","300033","300368","300307","600570","002368","600389","002402","002655","600547","601311","000858","300236","002460","000728","002746","300315","600150","603885","002048","600120","300242","300247","002047","600503","000937","002679","603799","300106","002438","300481","300251","300333","300052"]#"000538","300093",
Url = 'http://table.finance.yahoo.com/table.csv?s='
Dir = '/Users/Yang/Documents/Job/SelfCodeTool/Stock/HistoryStock/'


def downloadFile():
	if os.path.isdir(Dir):
		shutil.rmtree(Dir)
	os.mkdir(Dir)
	for index,value in enumerate(StockCode):
		StockInfo = {}
		code = ""
		value_int = int(value)
		if value_int > 600000:
			code = value + ".ss"
		else:
			code = value + ".sz"
		url = Url + code
		fileName = Dir + value + ".csv"
		urllib.urlretrieve(url, fileName)
		print str(index) + ".Finish : " + fileName

downloadFile() 