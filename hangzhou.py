# -*- coding: utf-8 -*-
import scrapy
import json
import scrapy
import logging
from bs4 import BeautifulSoup
from hzershoufang.settings import table
from hzershoufang.items import HzershoufangItem
import re

class HangzhouSpider(scrapy.Spider):
    name = 'hangzhou'
    base_url = 'https://hz.lianjia.com/ershoufang/'
    def start_requests(self):
        district = ['xihu','xiacheng','jianggan','gongshu','shangcheng','binjiang',
                    'yuhang','xiaoshan','xiasha']
        for elem in district:
            region_url = self.base_url + elem
            yield scrapy.Request(url=region_url, callback=self.page_navigate)
    def page_navigate(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        try:
            pages = soup.find_all("div", class_="house-lst-page-box")[0]
            if pages:
                dict_number = json.loads(pages["page-data"])
                max_number = dict_number['totalPage']
                for num in range(1, max_number + 1):
                    url = response.url + 'pg' + str(num) + '/'
                    yield scrapy.Request(url=url, callback=self.parse)
        except:
            logging.info("*******该地区没有二手房信息********")

    def parse(self, response):
        item =  HzershoufangItem()
        soup = BeautifulSoup(response.body, "html.parser")

        # 通过url辨认所在区域
        url1 = response.url

        url2 = url1.split('/')
        #print (table[url[-3]])
        #print (url1)
        item['Region'] = table[url2[-3]]

        #获取到所有子列表的信息
        house_info_list = soup.find_all(name="li", class_="clear")
        for info in house_info_list:
            item['Id'] = info.a['data-housecode']
            house_info = info.find_all(name="div", class_="houseInfo")[0]
            house_info = house_info.get_text()
            house_info = house_info.split('|')
            try:
                item['Garden'] = house_info[0]
                item['Layout'] = house_info[1]
                item['Size'] =re.findall( r'(\d+.\d+).*?',house_info[2])[0]
                item['Direction'] = house_info[3]
                item['Renovation'] = house_info[4]
                if len(house_info) > 5:
                    item['Elevator'] = house_info[5]
                else:
                    item['Elevator'] = ''
            except:
                print("数据保存错误")

            position_info = info.find_all(name='div', class_='positionInfo')[0]

            item['District'] = position_info.a.string
            position_info1= position_info.get_text()
            item['Floor'] = re.findall(r'.*?\(.(\d*).\).*?', position_info1)[0]
            item['Year'] =re.findall(r'.*?\(.\d*.\)(\d*).*?', position_info1)[0]


            price_info = info.find_all("div", class_="totalPrice")[0]
            item['Price'] = price_info.span.get_text()

            yield item