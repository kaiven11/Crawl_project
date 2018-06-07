# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixinItem(scrapy.Item):
    title=scrapy.Field()
    url=scrapy.Field()


class wenzhangItem(scrapy.Item):
    author=scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    gongzhonghao=scrapy.Field()
