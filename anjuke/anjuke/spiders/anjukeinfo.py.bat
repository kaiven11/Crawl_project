# -*- coding: utf-8 -*-
import scrapy
import win_unicode_console
win_unicode_console.enable()
from scrapy.loader import ItemLoader
from anjuke.items import AnjukeItem
from urllib.parse import quote
from anjuke.settings import KEY
class AnjukeinfoSpider(scrapy.Spider):
    '''This function parses a sample response. Some contracts are mingled
    with this docstring.

    @url https://bj.zu.anjuke.com/?kw=%E8%A7%92%E9%97%A8&cw=%E8%A7%92%E9%97%A8
    @returns items 1 16
    @scrapes title price trail
    '''
    name = 'anjukeinfo'
    allowed_domains = ['beijing.anjuke.com']
    start_urls = ['http://beijing.anjuke.com/']
    visited_set = set()


    def __init__(self):
        super().__init__()
        self.itemloader=None

    def start_requests(self):

        yield scrapy.Request(url='https://bj.zu.anjuke.com/?kw={}&cw={}'.format(quote(KEY),quote(KEY)),
                             callback=self.parse_house_info,
                             dont_filter=True
                             )


    # def parse_item(self,response):
    #
    #
    #
    #     property_item = response.xpath('//*[@id="list-content"]//div/h3/a//@href')
    #
    #     for property in property_item.extract():
    #         # start the property_item requests
    #         req= scrapy.Request(url=property, callback=self.parse_introduct, dont_filter=True)
    #
    #         yield req


    def parse_house_info(self, response):
        #gender the itemloader
        extra = {}
        item=AnjukeItem()
        # response = ItemLoader(item=AnjukeItem(), response=response)
        # title = response.xpath('//div[@class="zu-info"]//a[1]//@title').extract()
        # house_detail_url = response.xpath('//*[@id="list-content"]/div/div/h3/a//@href').extract()
        # base = response.xpath('//*[@id="list-content"]/div/div[1]/p/text()[1]').extract()
        # square = response.xpath('//*[@id="list-content"]/div/div[1]/p/text()[2]').extract()
        # floor = response.xpath('//*[@id="list-content"]/div/div[1]/p/text()[3]').extract()
        # contract = response.xpath('//*[@id="list-content"]/div/div[1]/p/text()[4]').extract()
        # direction = response.xpath('//*[@id="list-content"]/div//p[2]/span[2]').extract()
        # trail = response.xpath('//*[@id="list-content"]/div//p[2]/span[3]').extract()
        # price = response.xpath('//*[@id="list-content"]//div//p/strong').extract()
        # current_page = response.xpath('/html/body/div[5]/div[3]/div[3]/div/i[@class="curr"]//text()').extract()
        # 纵向抓取
        # item['title'] = title
        # item['house_detail_url'] = house_detail_url
        # item['base'] = base
        # item['square'] = square
        # item['floor'] = floor
        # item['contract'] = contract
        # item['direction'] = direction
        # item['trail'] = trail
        # item['price'] = price
        # item['current_page'] = current_page
        # next_page=response.xpath('/html/body/div[5]/div[3]/div[3]/div/i[@class="curr"]//following-sibling::a[not(contains(text(),"下一页"))]//@href').extract()
        # property_item = response.xpath('//*[@id="list-content"]//div/h3/a//@href')
        # yield item
        #垂直抓取页面链接
        # for page in next_page:
        #     if page not in self.visited_set:
        #         self.visited_set.add(page)
        #         req= scrapy.Request(url=page, callback=self.parse_house_info, dont_filter=True,)
        #
        #         yield req
                # for i in property_item.extract():
                #     yield scrapy.Request(url=i, callback=self.parse_introduct, meta={'extra': extra})





    def parse_introduct(self,response):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item=AnjukeItem()
        content=response.xpath('//div[@class="auto-general"]//text()').extract()
        extra = response.meta['extra']
        extra.update({'content':content})
        item.update(extra)
        print(item)
        yield item







