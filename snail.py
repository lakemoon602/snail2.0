# coding=utf-8
import requests
import sys
import re
import time
import threading
import os
from vul_apache import apache_server_status_disclosure_BaseVerify
from vul_bak import bak_check_BaseVerify
from vul_crossadmin import crossdomain_find_BaseVerify
from vul_dstore import ds_check_BaseVerify
from vul_git import git_check_BaseVerify
from vul_jspconf import jsp_conf_find_BaseVerify
from vul_idea import jetbrains_ide_workspace_disclosure_BaseVerify
from vul_svn import svn_check_BaseVerify
from vul_options import options_method_BaseVerify
from vul_other import other_check_BaseVerify


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
lock=threading.Lock()
max_thread=200
count=0
https="https://"
http="http://"
domains=[]

#获取域名
def getDomain(file):
    with open(file,'r',encoding='UTF-8') as f:
    	for line in f:
    		domains.append(line[:-1])
    	f.close()
            

def scan(domain):
    url=http+domain
    urls=https+domain
    apache_server_status_disclosure_BaseVerify(url).run()
    time.sleep(2)
    apache_server_status_disclosure_BaseVerify(urls).run()
    time.sleep(2)
    bak_check_BaseVerify(url).run()
    time.sleep(2)
    bak_check_BaseVerify(urls).run()
    time.sleep(2)
    git_check_BaseVerify(url).run()
    time.sleep(2)
    git_check_BaseVerify(urls).run()
    time.sleep(2)
    jetbrains_ide_workspace_disclosure_BaseVerify(url).run()
    time.sleep(2)
    jetbrains_ide_workspace_disclosure_BaseVerify(urls).run()
    time.sleep(2)
    jsp_conf_find_BaseVerify(url).run()
    time.sleep(2)
    jsp_conf_find_BaseVerify(urls).run()
    time.sleep(2)
    svn_check_BaseVerify(url).run()
    time.sleep(1)
    svn_check_BaseVerify(urls).run()
    time.sleep(2)
    ds_check_BaseVerify(url).run()
    time.sleep(2)
    ds_check_BaseVerify(urls).run()
    time.sleep(1)
    other_check_BaseVerify(url).run()
    time.sleep(2)
    other_check_BaseVerify(urls).run()
    #print("[-]"+domain+" 检测完毕")

if __name__=="__main__":

    print(banner)

    #获取域名
    getDomain(sys.argv[1])
    thread=[]
    #多线程调用
    #daemon参数，主线程随子线程结束还是子线程随主线程结束,默认为False
    start=time.time()
    for domain in domains:
        t=threading.Thread(target=scan,args=(domain,),daemon=True)
        thread.append(t)
    
    #维持线程队列
    for t in thread:
        t.start()
        while True:
            if len(threading.enumerate())<=max_thread:
                #print("当前线程数: "+str(len(threading.enumerate())),end="")
                time.sleep(1)
                break
    print(threading.enumerate())      
    while True:
        #print(len(threading.enumerate()))
        if len(threading.enumerate())==1:
            break
        time.sleep(5)
        
    print('[!]Detection over in '+str(time.time()-start).split('.')[0]+'s.')


