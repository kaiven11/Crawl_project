# -*- coding: utf-8 -*-
import scrapy
import win_unicode_console
win_unicode_console.enable()
from anjuke.items import AnjukeItem
from urllib.parse import quote
from anjuke.settings import KEY
class AnjukeinfoSpider(scrapy.Spider):

    name = 'anjukeinfo'
    allowed_domains = ['beijing.anjuke.com']
    start_urls = ['http://beijing.anjuke.com/']
    visited_set = set()
    def start_requests(self):

        yield scrapy.Request(url='https://bj.zu.anjuke.com/?kw={}&cw={}'.format(quote(KEY),quote(KEY)),
                             callback=self.parse_house_info,
                             dont_filter=True
                             )


    #parse the pageinfo and gender request for per page and current page
    def parse_house_info(self, response):
        '''This function parses a sample response. Some contracts are mingled
            with this docstring.
            @url https://bj.zu.anjuke.com/?kw=%E8%A7%92%E9%97%A8&cw=%E8%A7%92%E9%97%A8
            @returns requests 1 100
            @scrapes title price trail
        '''
        #gender all the house info
        item_list=response.xpath('//div[contains(@class,"zu-item")]')
        next_page = response.xpath(
            '/html/body/div[5]/div[3]/div[3]/div/i[@class="curr"]//following-sibling::a[not(contains(text(),"下一页"))]//@href').extract()
        for i in item_list:
                item = AnjukeItem()
                item['title'] = i.xpath('div[@class="zu-info"]//a[1]//@title')[0].extract().strip()
                item['house_detail_url'] = i.xpath('div[@class="zu-info"]//a[1]/@href')[0].extract().strip()
                base = i.xpath('div[@class="zu-info"]//p/text()[1]')[0].extract().strip()
                square = i.xpath('div[@class="zu-info"]//p/text()[2]')[0].extract().strip()
                floor = i.xpath('div[@class="zu-info"]//p/text()[3]')[0].extract().strip()
                contract = i.xpath('div[@class="zu-info"]//p/text()[4]')[0].extract().strip()
                direction = i.xpath('div[@class="zu-info"]//p[2]/span[2]')[0].extract().strip()
                try:
                    trail = i.xpath('div[@class="zu-info"]//p[2]/span[3]')[0].extract().strip()
                except:
                    trail="None"
                price = i.xpath('div[@class="zu-side"]//p/strong//text()')[0].extract().strip()
                current_page=response.xpath('/html/body/div[5]/div[3]/div[3]/div/i[@class="curr"]//text()').extract()
                item['base'] = base
                item['square'] = square
                item['floor'] = floor
                item['contract'] = contract
                item['direction'] = direction
                item['trail'] = trail
                item['price'] = price
                item['current_page']=current_page
                yield scrapy.Request(url=item['house_detail_url'],dont_filter=True,meta={'item':item},callback=self.parse_item)
        #crawl the nextpage
        for page in next_page:
            if page not in self.visited_set:
                self.visited_set.add(page)
                yield scrapy.Request(url=page, callback=self.parse_house_info, dont_filter=True,)
    #parse the property item
    def parse_item(self,response):
        content ="".join(response.xpath('//div[@class="auto-general"]//text()').extract()).strip()
        item=response.meta['item']
        item['content']=content
        yield item




