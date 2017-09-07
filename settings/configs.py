# coding:utf-8

# 测试环境还是生产环境
Environment = '测试'

# 根据网速，可以调整等待时间
rate = 1
ave_wait = 2*rate
long_wait = 5*rate
short_wait = 1*rate

# 生产环境是否可以用测试环境的dns？ （大部分都可以，在线客服不可以）
pro_dns_ok_used_at_test = True

cookieSavedFile = "business"
cookieTxtName = 'cookies.txt'