# coding:utf-8

import wmi

from settings import configs

#   需要安装 [ wmi , pypiwin32 ] （pip有时候安装不成功， 去pypi直接下载然后 py -3 setup.py install)

wmiService = wmi.WMI()
colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled=True)

# 调试用代码，打印出所有的object
# for objNicConfig in colNicConfigs:
#    print (objNicConfig.Index)
#    print (objNicConfig.SettingID)
#    print (objNicConfig.Description)
#    print (objNicConfig.IPAddress)
#    print (objNicConfig.IPSubnet)
#    print (objNicConfig.DefaultIPGateway)
#    print (objNicConfig.DNSServerSearchOrder)

if len(colNicConfigs) < 1:
    print('没有找到可用的网络适配器')
    exit()

# 获取第一个网络适配器的设置
objNicConfig = colNicConfigs[0]

# for method_name in objNicConfig.methods:
#   method = getattr(objNicConfig, method_name)
#   print method

# ----------------ip地址、网关等-------------------
arrIPAddresses = ['192.168.1.136']
arrSubnetMasks = ['255.255.0.0']
arrDefaultGateways = ['192.168.1.1']
arrGatewayCostMetrics = [1]


def modifyDNS(dns=['']):
    returnValue = objNicConfig.SetDNSServerSearchOrder(DNSServerSearchOrder=dns)
    if returnValue[0] == 0:
        print('  成功设置DNS')
    elif returnValue[0] == 1:
        print('  成功设置DNS')
        # intReboot += 1
    else:
        print('修改失败(DNS设置发生错误)')
        # print (returnValue[0])  调试代码。 打印出当前修改的object。
        exit()

dns_now = objNicConfig.DNSServerSearchOrder

#当dns和环境不符的时候，自动切换dns
#进化：测试的dns，生产通常可以用，生产的dns，测试用不了。

def checkDNS(tarEnv_str):
    if tarEnv_str == '生产':
        tarEnv_dns = ['114.114.114.114']
    elif tarEnv_str == '测试':
        tarEnv_dns = ['192.168.6.1']
    elif tarEnv_str == '外网':
        tarEnv_dns = ['8.8.8.8']
    else:
        print('环境的输入参数应该为“生产”，“测试”，“外网”')

    prompt_str = 'DNS已经修改为 %s'
    # 如果当前dns（dns now）和目标dns相等pass，
    if dns_now[0] == tarEnv_dns[0]:
        pass
    # 如果配置中，测试环境的dns生产也可以用，且要换生产环境，也pass
    elif configs.pro_dns_ok_used_at_test and tarEnv_dns[0] == '114.114.114.114':
        pass
    # 其他情况切换
    else:
        try:
            print('当前DNS为%s, DNS切换中，请稍后...' % dns_now[0])
            modifyDNS(tarEnv_dns)
            print(prompt_str % tarEnv_dns)
        except:
            print("DNS切换失败，请确认以管理员身份运行。")

