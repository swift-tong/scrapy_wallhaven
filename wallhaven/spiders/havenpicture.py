# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy import Request
import sys
from wallhaven.items import WallhavenItem


class HavenpictureSpider(scrapy.Spider):
    name = 'havenpicture'
    allowed_domains = ['https://alpha.wallhaven.cc/','https://alpha.wallhaven.cc/wallpaper/']
    start_urls = ['https://alpha.wallhaven.cc/toplist?']


    def start_requests(self):
        base_url='https://alpha.wallhaven.cc/toplist?'
        for i in range(1,self.settings.get('MAX_PAGE')+1):
            data={'page' : i}
            params=urlencode(data)
            url=base_url+params
            yield Request(url,self.parse)

    def parse(self, response):
        item=WallhavenItem()
        selector_li=response.xpath('//*[@id="thumbs"]/section[1]/ul/li')
        for sel in selector_li:
            detail=sel.xpath('./figure/a/@href').extract_first()
            print(detail)
            yield Request(detail,self.parse_detail,dont_filter=True)

    def parse_detail(self,response):
        print('enter parse_detail')
        item = WallhavenItem()
        author=response.xpath('//*[@id="showcase-sidebar"]/div/div[1]/div[2]/dl/dd[1]/a[2]/text()').extract_first()
        tages=response.xpath('//*[@id="tags"]/li/a/text()').extract()
        url='https:'+response.xpath('//*[@id="wallpaper"]/@src').extract_first()
        print(author)
        print(tages)
        print(url)
        item['author']=author
        item['tages']=tages
        item['url'] =url
        print('exit parse_detail')
        yield item