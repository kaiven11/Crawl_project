# -*- coding: utf-8 -*-
import scrapy
from weixin.items import WeixinItem,wenzhangItem
from scrapy.shell import inspect_response
import requests
import  re
from urllib import parse
def decrator(fun):
    def wrapper(*args,**kwargs):
        x=fun(*args, **kwargs)
        inspect_response()
        return  x
    return wrapper









class WenzhangSpider(scrapy.Spider):

    name = 'wenzhang'
    allowed_domains = ['weixin.sougou.com']
    start_urls = ['http://weixin.sougou.com/']



    cookies={
        "SUV":"001E436C7B711F9A5AE3188F73A33436",
        "IPLOC":"CN1100",
        "SUID":"6414767B2E08990A000000005AE68A551",
        "ABTEST":"0|1525093250|v1",
        "weixinIndexVisited": "1",
        "ppinf":"5|1525093311|1526302911|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTYlQjAlQjglRTklOUIlQjd8Y3J0OjEwOjE1MjUwOTMzMTF8cmVmbmljazoxODolRTYlQjAlQjglRTklOUIlQjd8dXNlcmlkOjQ0Om85dDJsdUhpdmtxczdhNFlyQ3kzckc5cE05U3dAd2VpeGluLnNvaHUuY29tfA",
        "pprdig":"b7zUzCjbhR89JD9U2CpKeyHIa9K2soCapAJZxLjNLAVInshH8cOTUwga1Yb184GE-SR2BxTUDNjGUq6r4-VYlO-W96WChfQqUWWQwxXgWTvKpN4CYh-Q5ZYu6BRqn43irdxoDwNRj6Kr5pUYlFQfiDCfdMfHrtVFnWpiIPnXEHo",
        "sgid":"11-34788047-AVrnE7iccZdSCjXWuWaoS6ics",
        "ld":"Akllllllll2zDqpaQsVS0VreUYHzDqpGWT9zRyllll9llllxjllll5@@@@@@@@@@",
        "cd":"15257644921 & 15c122711f46f37dc771d0e6bded697f",
        "rd":"0yllllllll2zioIUQmz3qqreUYHzDqpGWT9tLZllll9lllljjllll5@@@@@@@@@@",
        "GOTO":"Af22417-3002",
        "SNUID":"990A676B11157D1459868E1C11F5ABAF",
        "ppmdig":"1526144832000000f446b3c4f7bba589ff6a5901f506778c",
        "JSESSIONID":"aaaJVYAn4lr3BekZqbjnw1",
         "sct":"181",
        }


    def start_requests(self):
        '''
        the first url to access
        '''
        key='风景'
        url_encode=parse.quote(key)
        yield scrapy.Request(url="http://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=691&sst0=1526152462908&lkt=1%2C1526152462805%2C1526152462805".format(url_encode),
                             method='GET',callback=self.parse_article,
                             cookies=self.cookies,
                             dont_filter=True,
                             )

    def parse_content(self, response):
        '''
        parse the content,return the item
        '''
        content_raw=response.xpath('//div[@id="js_content"]//text()').extract()
        content="".join(content_raw)
        gongzhonghao=response.xpath('//*[@id="profileBt"]/a[1]//text()').extract()[0]
        author=response.xpath('//*[@id="meta_content"]/p//text()').extract()

        item=wenzhangItem()
        item['content']=content
        item['gongzhonghao']=gongzhonghao
        item['author']=author
        yield  item


    def parse_article(self, response):
        '''
        parse the url of the
        '''
        item=WeixinItem()
        a = re.sub('<em>|</em>|<!--red_beg-->|<!--red_end-->', '', response.text)
        #the title
        title=re.compile('<div class="txt-box">.*?<a.*?>(.*?)</a>',re.S).findall(a)
        #the url
        url=response.xpath('//ul[@class="news-list"]//li//h3//a/@href').extract()
        next_page=response.xpath('//div[@id="pagebar_container"]//a//@href').extract()
        #loop the next page list
        if next_page:
            for i in next_page:
                yield scrapy.Request(url="http://weixin.sogou.com/weixin"+i,cookies=self.cookies,callback=self.parse_article,dont_filter=True,meta={'referer':"http://weixin.sogou.com"})

        for k,v in enumerate(title):
            item['title']=v
            item['url']=url[k]
            yield item

        #request for article
        for u in url:
            yield scrapy.Request(u,cookies=self.cookies,callback=self.parse_content,dont_filter=True,meta={'referer':"http://weixin.sogou.com"})






