# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from scrapy import signals
from pydispatch import dispatcher


def item_type(item):
    # The CSV file names are used (imported) from the scrapy spider
    # return type(item)
    return type(item).__name__

class CaringPipeline(object):

    fileNameCsv = ['CityItem', 'CountryItem', 'CompanyItem']

    def __init__(self):
        self.files ={}
        self.exporters = {}
        # dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        # dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.files = dict([(name, open(f'{name}.csv', 'wb')) for name in self.fileNameCsv])
        for name in self.fileNameCsv:
            self.exporters[name] = CsvItemExporter(self.files[name])
            # self.exporters[name].start_exporting()
            if name == 'CityItem':
                self.exporters[name].fields_to_export = ['state', 'city', 'total']
            elif name == 'CountryItem':
                self.exporters[name].fields_to_export = ['state', 'country', 'total']
            elif name == 'CompanyItem':
                self.exporters[name].fields_to_export = ['state', 'country', 'name', 'service', 'total_review', 'star', 'review_text', 'description']
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):

        what = item_type(item)
        if what in set(self.fileNameCsv):
            self.exporters[what].export_item(item)
        return item
