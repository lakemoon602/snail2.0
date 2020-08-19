# snail2.0
usage: python snail.py domain.txt time

domain.txt 储存域名字典，一行一个
time  扫描延时，主要为防止BanIP,不想延时可以设置为0

至于线程，可以直接在snail.py 33行更改线程数

最后，由于该扫描器如其名——snail（蜗牛），扫描得很慢，所以推荐挂在服务器上: nohup python3 snail.py domain.txt 2 &

![image](https://cdn.nlark.com/yuque/0/2020/png/479381/1597846498604-699afbb3-672c-41bb-8c3e-cb92381e09e3.png)
