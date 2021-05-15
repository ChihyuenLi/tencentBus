#!/usr/bin/python
# coding=utf-8

#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

import csv
import os
import io,re,requests,json
buslist = []
with io.open('上班路线.csv','r',encoding='utf-8') as f:
	reader  =csv.reader(f)
	key_word = "科兴大厦"
	for row in f :
		if key_word in row:
			buslist.append(row)

#print len(buslist)
counts = {}
for item in buslist:
	#只保留班车路线，班车车次和出发时间不需要
	bus_line = item.split(',')[2]
	#去除括号
	bus_line = re.sub("\(.*?\)", "", bus_line)
	#分割各个站点，并存入字典里
	bus_station = bus_line.split("→")
	for i in bus_station:
		if i in counts:
			counts[i] +=1
		else:
			counts[i] = 1
counts = sorted(counts.items(),  key=lambda d: d[1], reverse=False)

def addressName_to_gps(address):
	URL = 'https://restapi.amap.com/v3/geocode/geo?address='+address+'&city=深圳&output=json&key=1ff006deb10be4bceceff35732b89160'
	res = requests.get(URL).text
	a = json.loads(res)
#	print (address,res)
	try:
		location =a['geocodes'][0]['location']
	except:
		print (address)
		location=0	
	return location

gps = {}#{名称，gps坐标}	
for k,v in counts:
	res = addressName_to_gps(str(k))
	gps[k] = res
#	print (k,res)
with open("站点坐标.txt",'w') as f1:
	for k,v in counts:
		line = str(k)+"   "+str(v)+"   "+str(gps[k])+'\n'
		f1.write(line)
		print (line)