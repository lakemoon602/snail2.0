#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: .DS_store文件泄露扫描
referer: unknown
author: Lucifer
description: 忘记了删除.DS_store文件。
'''
import sys
import requests

class ds_check_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/.DS_Store"
        vulnurl = self.url + payload
        domain=self.url.split("/")[2]
        tag=4
        try:
            req = requests.get(vulnurl, headers=headers, timeout=1)
            req.encoding = req.apparent_encoding
            if r"ShowStatusBar" in req.text and req.status_code==200:
                print("[+]存在.DS_store文件泄露漏洞(低危)\t"+vulnurl)
                return [domain,tag,payload]
            else:
                return False

        except:
            return False

if __name__ == "__main__":
    testVuln = ds_check_BaseVerify(sys.argv[1])
    print(testVuln.run())
