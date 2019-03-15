

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base 


MYSQL_URL = 'mysql+pymysql://root:qwerasdf@localhost:3306/alibaba?charset=utf8'

engine = create_engine(MYSQL_URL)  
Base = declarative_base()
Session = sessionmaker(bind=engine)
 
class Product(Base):
	__tablename__ = 'product'
	id = Column(Integer, primary_key=True)
	img = Column(String(200))
	price = Column(String(200))
	title = Column(String(200),nullable=False)
	shop = Column(String(100))

class SqlalchemyCls(object):
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def query(self, title, shop):
        # 检查数据库是否有该记录
        res = self.session.query(Product).filter_by(title=title,shop=shop).first()
        return res

if __name__ == "__main__":
	# 建表
	Product.metadata.create_all(engine)

	# 查询
	# mysql = SqlalchemyCls()
	# res = mysql.query('100纯棉圆领精梳大码宽松短袖T恤印logo文化衫定制活动广告衫定做','sntslzy')
	# print(res)
