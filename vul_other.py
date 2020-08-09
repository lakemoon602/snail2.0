#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: 源码泄露扫描
referer: unknown
author: Lucifer
description: 忘记了删除源码。
'''
import sys
import requests
import time

class other_check_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payloads=[]
        with open('dicts.txt','r') as f:
            for line in f:
                payloads.append("/"+line[:-1])
            f.close()

        for payload in payloads:
            time.sleep(1)
            try:
                vulnurl = self.url + payload
                domain=self.url.split("/")[2]
                tag=1
                req=requests.head(vulnurl,headers=headers,timeout=1)
                if req.status_code==200 and int(req.headers["Content-Length"])>=1000000:
                    print("[+]存在敏感文件泄露(高危)\t"+vulnurl)
                    return [domain,tag,payload]
            except:
                pass
        return False

if __name__ == "__main__":
    testVuln = other_check_BaseVerify(sys.argv[1])
    print(testVuln.run())
