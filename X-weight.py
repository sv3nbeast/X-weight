import requests
import re
import getopt
import sys
import threadpool
import urllib.request
#!/usr/bin/python3
import hashlib
import urllib3
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context



def getPc(domain):
    try:
 

        aizhan_pc = 'https://baidurank.aizhan.com/api/br?domain={}&style=text'.format(domain)
        # b = requests.post(url=post_url,headers=headers, proxies=proxy, timeout = 7)
        res = urllib.request.urlopen(aizhan_pc,timeout=10)
        # res = opener.open(aizhan_pc,timeout=10)
        a = res.read().decode('UTF-8')
        result_pc = re.findall(re.compile(r'>(.*?)</a>'),a)
        pc = result_pc[0]
    except Exception as u:
        print(u)
        pc = '0'
    return pc

def getMobile(domain):
    try:

        aizhan_pc = 'https://baidurank.aizhan.com/api/mbr?domain={}&style=text'.format(domain)
        # b = requests.post(url=post_url,headers=headers, proxies=proxy, timeout = 7)
        res = urllib.request.urlopen(aizhan_pc,timeout=10)
        # res = opener.open(aizhan_pc,timeout=10)
        a = res.read().decode('UTF-8')
        result_m = re.findall(re.compile(r'>(.*?)</a>'),a)
        mobile = result_m[0]
    except Exception as u:
        print(u)
        mobile = '0'
    return mobile
# 权重查询
def seo(name,url):

    try:

        result_pc = getPc(name)
        result_mobile = getMobile(name)

    except Exception as u:
        print(u)
        result_pc = '0'
        result_mobile = '0'

        print('[- 目标{}获取权重失败,自动设为0'.format(url))
    # print('运行正常')
    print('[+ 百度权重:'+result_pc+'  移动权重:'+result_mobile+'  Url:'+url)
    with open('vul.txt','a',encoding='utf-8') as y:
        y.write('['+result_pc+','+result_mobile+','+url+']'+'\n')

    return True

def exp(name1):
    # opts, args = getopt.getopt(sys.argv[1:], '-u:-r:', ['url', 'read'])
    # print(name1)
    try:
        name = name1[name1.rfind('/'):].strip('/')
        # print(name)
        rew = seo(name,name1)

    except Exception as u:
    # except:
        print(u)
        print('[- 目标{}检测失败，已写入fail.txt等待重新检测'.format(name1))
        # file_fail.write(name1+'\n')
        with open('fail.txt',mode='a',encoding='utf-8') as o:
            o.write(name1+'\n')


def multithreading(funcname, params=[], filename="ip.txt", pools=15):
    works = []
    with open(filename, "r") as f:
        for i in f:
            func_params = [i.rstrip("\n")] + params
            works.append((func_params, None))
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(funcname, works)

    [pool.putRequest(req) for req in reqs]
    pool.wait()

def main():
    multithreading(exp, [], "ip.txt", 15)  # 默认15线程
    print("全部check完毕，请查看当前目录下的vul.txt")

if __name__ == "__main__":
    # st = False
    # main(st)
    main()