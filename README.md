# AutoDector

一个爬虫抓取调研的自动化分析工具。

使用场景：
  给定url和一堆header，用来确认哪些header是正确下载这个url所必须的。

用法：
  header信息，可以直接在浏览器debug->Network相应的http请求中截取request而得来，存入文件中。
  通过must_contain，给定一些标识字符串，来界定每次的抓取尝试是否符合预期。
