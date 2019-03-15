


import redis


HOST = "127.0.0.1"
PORT = 6379
PASSWORD = ''

r = redis.StrictRedis(host=HOST,port=PORT, password=PASSWORD)

r.set('name', 'test')
r.set('title', 'hahah')