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

# cookie保存的文件夹和名字
cookieSavedFile = "business"
cookieTxtName = 'cookies.txt'

# log保存的地方
log_file = 'test_log.txt'

# 是否打印日志
printLog = True

# 是否生成测试报告
generateReport = True

# 是否在控制台输出日志
outputLog = True

# 网上抓还是本地获取
onlinePoem = False