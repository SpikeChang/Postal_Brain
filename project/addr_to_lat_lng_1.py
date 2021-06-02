import requests
import json
import codecs
import csv
import os
import sys
import time
from requests.adapters import HTTPAdapter as adapter

class GeoCode:
    '''
    批量文件经纬度转换
    '''
    def __init__(self, url, key, path, count, session):
        self.url = url
        self.key = key
        self.path = path
        self.count = count
        self.session = session

    def getJson(self):
        try:
            self.json = requests.get(self.this_url).json()
        except:
            self.getJson()

    def getGeo(self, address, i):
	
        print(i)
        #最后一个字符串为api key
        self.this_url = self.url + address + '&key=' + self.key
        
        #不断发送网络请求直到请求被响应
        self.getJson()
            
        if self.json['status'] == '1':
            if len(self.json['geocodes']) > 0:
                GPS = self.json['geocodes'][0]['location']
                lng = GPS.split(',')[0]
                lat = GPS.split(',')[1]
                self.writer.writerow([str(i), lng, lat])
            else:
                self.writer.writerow([str(i), '', ''])
        else:
            self.writer.writerow([str(i), '', ''])

    def readFile(self):
        #读取需要转换的地址
        fr = codecs.open('input/' + self.path, 'r', 'gb18030', errors='ignore')
        self.reader = csv.reader(fr)

    def geoFile(self):
        
        date = time.strftime('%Y-%m-%d')
        fw = open('output/' + self.path, 'a+',encoding='utf-8', newline='')
        self.writer = csv.writer(fw)

        index = 0 # start point
        limit = index + 3000000 # end point
        count = 0 # 用于保存网络不好时，中断在何处
        with open(self.count, 'r') as f:
            count = int(f.readline())

        i = 0
        for line in self.reader:
            #使i到达需要处理的行
            if i < index + count:
                i = i + 1
                continue

            try:
                if line[10] == '':
                    self.getGeo(line[8], i)
                else:
                    self.getGeo(line[10], i)
            except:
                self.getGeo(line[2], i)
                
            #保存中断处
            count += 1
            with open(self.count, 'w') as f:
                f.write(str(count))
            if i == limit:
                break
            i = i + 1

if __name__ == '__main__':

    url = "http://restapi.amap.com/v3/geocode/geo?output=json&address="
    key = '82a84c6de7beb9254fe5167542c5dba1'
    with open('input/file_path.txt', 'r') as f: # 读取需要处理的文件的路径
        path = f.readlines()[0].strip('\n')
    count = 'buffer/num1.txt'
    #设置超时session
    session = requests.Session()
    session.mount('http://', adapter(max_retries=3))
    session.mount('https://', adapter(max_retries=3))

    geocode = GeoCode(url, key, path, count, session)
    geocode.readFile()
    geocode.geoFile()
    sys.stdout.write('Done!')