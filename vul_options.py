#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: options方法开启
description: 
'''
import sys
import requests


class options_method_BaseVerify:
    def __init__(self, url):
        self.url = url

    def run(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        vulnurl = self.url
        try:
            req = requests.options(vulnurl, headers=headers, timeout=1)

            if r"OPTIONS" in req.headers['Allow']:
                print("[+]存在options方法开启(敏感信息)\t"+vulnurl+"\tAllow:"+req.headers['Allow'])
            else:
                return "[-]NO vuln!"
        except:
            return "[-] ======>连接超时"

if __name__ == "__main__":
    testVuln = options_method_BaseVerify(sys.argv[1])
    testVuln.run()