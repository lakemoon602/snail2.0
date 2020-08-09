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
    
    name=name.split('/')[2]
    pres=name.split('.')

    com=pres[0]+pres[1]
    com1=None
    if len(pres)>4:
        com1=pres[0]+pres[1]+pres[2]

    for ext in exts:
        res.append("/"+com+ext)
        #print(com+ext)
        if com1:
            res.append("/"+com1+ext)
        res.append("/"+name+ext)
        #print(name+ext)
        for pre in pres:
            res.append("/"+pre+ext)
            #print(pre+ext)
    return res

class bak_check_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        domain=self.url.split("/")[2]
        tag=1
        payloads = genWeak(self.url)
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
    testVuln = bak_check_BaseVerify(sys.argv[1])
    testVuln.run()
