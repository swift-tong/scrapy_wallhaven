# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import sys


class WallhavenPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        #[(True, {'url': 'https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-704981.jpg', 'path': 'wallhaven-704981.jpg', \
        #  'checksum': '9cca2638f23b53af592ba68cc98d6dfd'})]
        print("results:")
        print(results)
        print("item:")
        print(item)
        print("info:")
        print(info)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        yield Request(item['url'])
