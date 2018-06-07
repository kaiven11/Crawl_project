# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JiandanItem(scrapy.Item):
    image_urls = scrapy.Field()#should be list
    images = scrapy.Field()

