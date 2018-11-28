# AutoDector

一个爬虫抓取调研的自动化分析工具。

## 使用场景
给定url和一堆header，用来确认哪些header是正确下载这个url所必须的。

header信息，可以直接在浏览器debug->Network相应的http请求中截取request而得来，存入文件中。
通过must_contain，给定一些标识字符串，来界定每次的抓取尝试是否符合预期。

## 使用举例
python detector.py -u "https://blog.csdn.net/u012005313/article/details/50111455" -m "python Argparse" -f headers.txt

返回如下：
```shell
[2018-11-28 17:04:47] CONTENT_NOT_OK, try_without:Accept-Language
====== useful headers =======
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,ko;q=0.6,zh-TW;q=0.5,fr;q=0.4
```
