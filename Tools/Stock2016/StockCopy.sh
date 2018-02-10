python /Users/Yang/Documents/Job/SelfCodeTool/Stock/StockData.py

SourceDir="/Users/Yang/Documents/Job/SelfCodeTool/Stock/Output/"
FileName=`date +%Y-%m-%d`
TargetDir="/Users/Yang/Documents/Self_Examination/大盘预测/StockData/DetailData"
SoruceFile=$SourceDir$FileName
cp -f $SoruceFile $TargetDir
echo $FileName"已经复制到"$TargetDir