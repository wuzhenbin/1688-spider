# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    img = Column(String(200))
    price = Column(String(200))
    title = Column(String(200),nullable=False)
    shop = Column(String(100))

class SqlalchemyPipeline(object):
    def __init__(self, mysql_url):
        engine = create_engine(mysql_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def add_one(self, item):
        # 检查数据库是否有该记录
        res = self.session.query(Product).filter_by(title=item['title'],shop=item['shop']).first()
        if not res:
            new_obj = Product(
                title=item['title'],
                img=item['img'],
                price=item['price'],
                shop=item['shop'],
            )
            self.session.add(new_obj)
            self.session.commit()
            return new_obj
        else:
            print('{}:该记录已存在！{}'.format(res.id,res.title))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_url = crawler.settings.get('MYSQL_URL')
        )

    def process_item(self, item, spider):
        self.add_one(item)
        return item


class AlibabaPipeline(object):
    def process_item(self, item, spider):
        if 'title' in item:
            pattern = re.compile(r'<[^>]+>',re.S)
            item['title'] = pattern.sub('',item['title'])
        return item