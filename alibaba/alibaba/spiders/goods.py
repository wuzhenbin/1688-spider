# -*- coding: utf-8 -*-
from scrapy import Spider, Request, cmdline
from alibaba.items import ProductItem
from urllib.parse import urlencode
import json
import re
from urllib.parse import  unquote, quote


class GoodsSpider(Spider):
    name = 'goods'
    allowed_domains = ['data.p4psearch.1688.com']
    base_url = 'https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?'

    def start_requests(self):
        keywords = self.settings.get('KEYWORDS')
        for keyword in keywords:
            keyword_to_url = quote(keyword)
            for page in range(100):
                for zpage in range(6):
                    params = {
                        'beginpage': page+1,
                        'asyncreq': zpage+1,
                        'keywords': keyword_to_url,
                    }
                    url = self.base_url + urlencode(params)
                    yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        res = json.loads(response.body)
        lis = res['data']['content']['offerResult']

        for item in lis:
            product = ProductItem()
            product['title'] = item['title']
            product['shop'] = item['loginId']
            product['price'] = item['strPriceMoney']
            product['img'] = item['imgUrl']
            yield product

if __name__ == '__main__':
    cmdline.execute("scrapy crawl goods".split())