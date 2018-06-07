# -*- coding: utf-8 -*-
from scrapy import  Request
import scrapy
# import win_unicode_console
# win_unicode_console.enable()
from jiandan.items import JiandanItem
import logging
from utils.getlogger import get_logger
class JiandanspiderSpider(scrapy.Spider):
    name = 'jiandanspider'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/']
    def start_requests(self):
        yield Request(url='http://jandan.net/ooxx',callback=self.parse,dont_filter=True)
    def parse(self, response):
        #imgage urls
        img_list=response.xpath('//*[contains(@id,"comment-")]')
        next_page=response.xpath('//*[@id="comments"]//div/a[contains(text(),"下一页")]//@href')[0].extract()
        for img in img_list:
            item=JiandanItem()
            img_url=img.xpath('.//div//img//@src').extract()
            item['image_urls']=img_url
            yield item

        #the next page
        if next_page:
            yield Request(url="http:"+next_page,dont_filter=True,callback=self.parse)