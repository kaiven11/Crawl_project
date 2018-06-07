# -*- coding: utf-8 -*-
from openpyxl import Workbook
from w3lib.html import remove_tags
class JsonWriterPipeline(object):
    '''
    write items into excel file
    @:return item
    '''
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['标题','房源地址','地铁线', '价格','室/厅','面积', '楼层','联系人','朝向','基本信息','当前页'])  # 设置表头


    def process_item(self, item, spider):
        try:
            line = [item['title'],item['house_detail_url'],remove_tags(item['trail']),item['price'],
                    remove_tags(item['base']),item['square'],item['floor'],item['contract'],remove_tags(item['direction']),item['content'],item['current_page'][0],
                    ]  # 把数据中每一项整理出来
            self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        except IndexError as e:
           print(e)
        self.wb.save('tuniu.xlsx')  # 保存xlsx文件
        return item
