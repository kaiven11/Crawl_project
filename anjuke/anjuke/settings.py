# -*- coding: utf-8 -*-

BOT_NAME = 'anjuke'

SPIDER_MODULES = ['anjuke.spiders']
NEWSPIDER_MODULE = 'anjuke.spiders'

DEFAULT_REQUEST_HEADERS = {
    'accept': 'image/webp,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.8',
    'referer': 'https://beijing.anjuke.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
}
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3
COOKIES_ENABLED = True
ITEM_PIPELINES = {
   'anjuke.pipelines.JsonWriterPipeline': 300,
}

KEY="角门"