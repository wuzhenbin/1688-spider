
import requests
import json
from requests.exceptions import RequestException
from urllib.parse import urlencode
import time
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
}

def get_response(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print('err: %s' % e)

def parse_page(html):
	res = json.loads(html)
	lis = res['data']['content']['offerResult']

	for item in lis:
		pattern = re.compile(r'<[^>]+>',re.S)
		title = pattern.sub('',item['title'])

		yield {
			'title': title,
			'shop': item['loginId'],
			'price': item['strPriceMoney'],
			'img': item['imgUrl']
		}


def main():
	times = int(round(time.time() * 1000))
	keywords_ = '茶叶'
	keywords = keywords_
	params = {
		# 当前页码
		'beginpage': 2,
		# 当前子页码 一个beginpage 有6个asyncreq
		'asyncreq': 1,
		'keywords': keywords,
		# sortType=
		# descendOrder=
		# province=
		# city=
		# priceStart=
		# priceEnd=
		# dis=

		# 次要参数
		# cosite: 'baidujj',
		# 'location': 're',
		# 'callback': 'jsonp_1552387531620_83004',
		# 'trackid': '8856886241459804884118',
		# 'spm': 'a2609.11209760.j3f8podl.e5rt432e',
		# 'keywordid': '57065993601',
		# 'pageid': '6bcb51e048iARp',
		# 'p4pid': '1552387531017239008785',
		# '_': times
	}
	base_url = 'https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?'
	url = base_url + urlencode(params)
	html = get_response(url)
	if html:
		for item in parse_page(html):
			print(item)

if __name__ == '__main__':         
	main()