# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HzershoufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Id = scrapy.Field()
    #Region = scrapy.Field()
    Garden = scrapy.Field()
    Layout = scrapy.Field()
    Size = scrapy.Field()
    Direction = scrapy.Field()
    Renovation = scrapy.Field()
    Elevator = scrapy.Field()
    Floor = scrapy.Field()
    Year = scrapy.Field()
    Price = scrapy.Field()
    District = scrapy.Field()
    Region=scrapy.Field()