# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
import logging
from jiandan import settings
import os
from urllib import request
from utils.getlogger import get_logger
class JiandanPipeline(object):
    # def __init__(self):
    #     path=os.path.join(os.path.dirname(os.path.dirname(__file__)),"jiandan.log")
    #     if not os.path.exists(path):
    #         os.mknod("jiandan.log",mode=666)
    #     self.logger=get_logger("mylog",level=logging.DEBUG,File=True,path=path)
    def process_item(self, item, spider):
        # save path
        dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for image_url in item['image_urls']:
            list_name = image_url.split('/')
            file_name = list_name[len(list_name) - 1]
            file_path = '%s/%s' % (dir_path, file_name)
            if os.path.exists(file_name):
                continue
            with open(file_path, 'wb') as file_writer:
                try:
                    # download image
                    conn = request.urlopen(image_url,timeout=5)
                    file_writer.write(conn.read())
                except (TimeoutError,ValueError) as e:
                    pass
                    # self.logger.info("This URL %s Can't DonwLoad!"%image_url)
            file_writer.close()
        return item