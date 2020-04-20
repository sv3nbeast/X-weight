import requests #斯文
import re
import getopt
import sys
import threadpool
import urllib.parse
import urllib.request
#!/usr/bin/python3
import ssl
from urllib.error import HTTPError,URLError
import time
ssl._create_default_https_context = ssl._create_stdlib_context


headers={
'Host': 'baidurank.aizhan.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
'Sec-Fetch-Dest': 'document',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Cookie': ''
}


def getPc(domain):
    aizhan_pc = 'https://baidurank.aizhan.com/api/br?domain={}&style=text'.format(domain)
    try:

        req = urllib.request.Request(aizhan_pc, headers=headers)
        response = urllib.request.urlopen(req,timeout=10)
        b = response.read()
        a = b.decode("utf8")
        result_pc = re.findall(re.compile(r'>(.*?)</a>'),a)
        pc = result_pc[0]
        
    except HTTPError as u:
        time.sleep(3)
        return getPc(domain)

    return pc

def getMobile(domain):
    aizhan_pc = 'https://baidurank.aizhan.com/api/mbr?domain={}&style=text'.format(domain)
    try:
        # b = requests.post(url=post_url,headers=headers, proxies=proxy, timeout = 7)
        # res = urllib.request.urlopen(aizhan_pc,timeout=10)
        # # res = opener.open(aizhan_pc,timeout=10)
        # a = res.read().decode('UTF-8')
        req = urllib.request.Request(aizhan_pc, headers=headers)
        response = urllib.request.urlopen(req,timeout=10)
        b = response.read()
        a = b.decode("utf8")
        result_m = re.findall(re.compile(r'>(.*?)</a>'),a)
        mobile = result_m[0]
    except HTTPError as u:
        time.sleep(3)
        return getMobile(domain)


    return mobile
# 权重查询
def seo(name,url):

    try:

        result_pc = getPc(name)
        result_mobile = getMobile(name)

    except Exception as u:
        # print(u)
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
