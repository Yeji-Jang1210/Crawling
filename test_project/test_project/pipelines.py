# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from imp import reload

from itemadapter import ItemAdapter
from __future__ import unicode_literals

from scrapy.exporters import JsonItemExporter, CsvItemExporter

#import sys
import csv
# reload(sys)
# sys.setdefaultencoding('utf-8')

class TestProjectPipeline:
    def __init__(self):
        self.file = open("CompanyCrawlerFile.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding = 'euc-kr')
        self.exporter.start_exporting()
        # self.csvwriter = csv.writer(open("oxford_dictionary_new.csv","w"))
        # self.csvwriter.writerow(["title_list"])
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        # row = []
        # row.append(item["title_list"])
        # self.csvwriter.writerow(row)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()  # 파일 CLOSE

