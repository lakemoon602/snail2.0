#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 源码泄露扫描
description: 忘记了删除源码。
'''
import sys
import requests
import time


#生成敏感字典
def genWeak(name):
    exts=['.rar','.zip','.7z','.tar','.tar.7z','.tar.gz','.tar.bz2','.tgz']
    res=[]
    
    element=name.split('.')
    #print(element)
    for ext in exts:
        domain=""
        for ele in element:
            res.append(ele+ext)
            domain+='.'+ele
            res.append(domain+ext)
    data=[]
    for s in res:
        data.append(s.strip('.'))
    data=list(set(data))
    # res=map(lambda s:s.strip('.'),res)
    # 疑惑
    #print(data)
    return data

class bak_check_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        domain=self.url.split("/")[2]
        tag=1
        payloads = genWeak(domain)
        for payload in payloads:
            time.sleep(1)
            try:
                vulnurl = self.url + payload
                req=requests.head(vulnurl,headers=headers,timeout=1)
                if req.status_code==200 and int(req.headers["Content-Length"])>=1000000:
                    print("[+]存在源码泄露\t"+vulnurl)
                    return [domain,tag,payload]
            except:
                pass
        return False

if __name__ == "__main__":
    testVuln = bak_check_BaseVerify("http://www.nankai.edu.cn")
    testVuln.run()
