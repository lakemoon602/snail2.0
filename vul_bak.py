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
    com1=name.split('.')[1]
    com2=name.split('.')[0]+name.split('.')[0]
    for ext in exts:
        res.append("/"+name+ext)
        res.append("/"+com1+ext)
        res.append("/"+com2+ext)
    return res

class bak_check_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payloads = genWeak(self.url)
        for payload in payloads:
            time.sleep(1)
            try:
                vulnurl = self.url + payload
                req=requests.head(vulnurl,headers=headers,timeout=1)
                if req.status_code==200 and int(req.headers["Content-Length"])>=1000000:
                    print("[+]存在源码泄露\t"+vulnurl)
                    return
            except:
                pass
        return "[-]NO vuln!"

if __name__ == "__main__":
    testVuln = bak_check_BaseVerify(sys.argv[1])
    print(testVuln.run())
