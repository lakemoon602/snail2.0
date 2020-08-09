#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: svn源码泄露扫描
referer: unknown
author: Lucifer
description: 忘记了删除.svn目录而导致的漏洞。
'''
import re
import sys
import requests


class svn_check_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        payload = "/.svn/entries"
        vulnurl = self.url + payload
        domain=self.url.split("/")[2]
        tag=3
        try:
            req = requests.get(vulnurl, headers=headers, timeout=1, allow_redirects=False)
            if req.status_code==200 and (req.text=="12\n" or req.headers['Content-Length'] and req.headers['Content-Type']=="application/octet-stream"):
                print("[+]存在svn源码泄露(高危)"+vulnurl)
                return [domain,tag,payload]
        except:
            return False

if __name__ == "__main__":
    testVuln = svn_check_BaseVerify(sys.argv[1])
    testVuln.run()
