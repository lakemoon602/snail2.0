# coding=utf-8
# python snail.py domains.txt timeout //timeout代表延时
import requests
import sys
import re
import time
import threading
import os
import sqlite3
import json
from threadpool import ThreadPool,makeRequests
from vul_apache import apache_server_status_disclosure_BaseVerify
from vul_bak import bak_check_BaseVerify
from vul_dstore import ds_check_BaseVerify
from vul_git import git_check_BaseVerify
from vul_idea import jetbrains_ide_workspace_disclosure_BaseVerify
from vul_svn import svn_check_BaseVerify
from vul_other import other_check_BaseVerify
from db import DB

banner='''
   _____                   _   _ 
  / ____|                 (_) | |
 | (___    _ __     __ _   _  | |
  \___ \  | '_ \   / _` | | | | |
  ____) | | | | | | (_| | | | | |
 |_____/  |_| |_|  \__,_| |_| |_|
                                 
                                 
[!]start threading snail
[!]Dection starting...
'''
max_thread=150
https="https://"
http="http://"
domains=[]
time_out=0
pool = ThreadPool(max_thread) # 设置线程池

#获取域名
def getDomain(file):
    with open(file,'r',encoding='UTF-8') as f:
    	for line in f:
    		domains.append(line[:-1])
    	f.close()
            
#百度云观测接口
def baiduyun(domain):
    try:
        res=requests.get("http://ce.baidu.com/index/getRelatedSites?site_address="+domain)
        data=json.loads(res.text)
        domain=[]
        for value in data["data"]:
            domain.append(value["domain"])
        return domain
    except:
        return domain

#爬取域名，加入队列
def spider(url,time_out):
    try:
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        rex=url.split('.')
        if rex[-1]=="com":
            s=rex[-2]+"."+rex[-1]
        elif rex[-1]=="cn":
            if rex[-2] in ["gov","edu"]:
                s=rex[-3]+"."+rex[-2]+"."+rex[-1]
        patt=re.compile(r"http[s]?:.{1,40}."+s)
        res=requests.get(url,headers=headers,timeout=3)
        data=patt.findall(res.text)
        data=list(set(data))
        tmp=[]
        for d in data:
            d=d.split("/")[2]
            if d not in domains:
                domains.append(d)
                tmp.append(d)
        if len(tmp)==0:
            return
        if len(tmp)==1:
            #params=[[tmp,time_out],None]
            #request = makeRequests(scan, params)
            #[pool.putRequest(req) for req in request]
            return
        params = [([d, time_out], None) for d in tmp]
        request = makeRequests(scan, params)
        [pool.putRequest(req) for req in request]
    except:
        pass

def is_live(url):
    headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
    try:
        resp=requests.get(url,headers,timeout=3)
        return True
    except:
        return False

def scan(domain,timeout):
    url=http+domain
    urls=https+domain
    db=DB()

    #检测数据库是否已存在记录
    if db.check(domain):
        return False

    #百度云观测窗口获取子域名
    baidu=baiduyun(domain)
    tmp=[]
    for si in baidu:
        if si not in domains:
                domains.append(si)
                tmp.append(si)
    if len(tmp)!=0 and len(tmp)!=1:
        params = [([d, timeout], None) for d in tmp]
        request = makeRequests(scan, params)
        [pool.putRequest(req) for req in request]

    if is_live(url):
        #抓取链接
        spider(url,timeout)
        time.sleep(1)
        res=apache_server_status_disclosure_BaseVerify(url).run()
        if res:
            db.insert(res[0],res[1],res[2])
            return True
        time.sleep(timeout)
        res=bak_check_BaseVerify(url).run()
        if res:
            db.insert(res[0],res[1],res[2])
            return True
        time.sleep(timeout)
        res=git_check_BaseVerify(url).run()
        if res:
            db.insert(res[0],res[1],res[2])
            return True
        time.sleep(timeout)
        res=jetbrains_ide_workspace_disclosure_BaseVerify(url).run()
        if res:
            db.insert(res[0],res[1],res[2])
            return True
        time.sleep(timeout)
        res=svn_check_BaseVerify(url).run()
        if res:
            db.insert(res[0],res[1],res[2])
            return True
        time.sleep(timeout)
        res=ds_check_BaseVerify(url).run()
        if res:
            db.insert(res[0],res[1],res[2])
            return True
        time.sleep(timeout)
        res=other_check_BaseVerify(url).run()
        if res:
            db.insert(res[0],res[1],res[2])
            return True

    if not is_live(urls):
        db.insert(domain,0,'null')
 
    spider(urls,timeout)
    time.sleep(1)
    res=apache_server_status_disclosure_BaseVerify(urls).run()
    if res:
        db.insert(res[0],res[1],res[2])
        return True
    time.sleep(timeout)
    res=bak_check_BaseVerify(urls).run()
    if res:
        db.insert(res[0],res[1],res[2])
        return True
    time.sleep(timeout)
    res=git_check_BaseVerify(urls).run()
    if res:
        db.insert(res[0],res[1],res[2])
        return True
    time.sleep(timeout)
    res=jetbrains_ide_workspace_disclosure_BaseVerify(urls).run()
    if res:
        db.insert(res[0],res[1],res[2])
        return True
    time.sleep(timeout)
    res=svn_check_BaseVerify(urls).run()
    if res:
        db.insert(res[0],res[1],res[2])
        return True
    time.sleep(timeout)
    res=ds_check_BaseVerify(urls).run()
    if res:
        db.insert(res[0],res[1],res[2])
        return True
    time.sleep(timeout)
    res=other_check_BaseVerify(urls).run()
    if res:
        db.insert(res[0],res[1],res[2])
        return True
    # 检测完成
    db.insert(domain,0,'null')

if __name__=="__main__":

    print(banner)
    #获取域名
    getDomain(sys.argv[1])
    # 去重
    domains=list(set(domains))
    timeout=int(sys.argv[2])
    thread=[]
    #多线程调用
    start=time.time()
    params = [([d, timeout], None) for d in domains]
    request = makeRequests(scan, params)
    [pool.putRequest(req) for req in request]
    pool.wait()
    #while True:
     #   pass
    print('[!]Detection over in '+str(time.time()-start).split('.')[0]+'s.')


