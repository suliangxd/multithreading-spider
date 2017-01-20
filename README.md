#multithreading-spider
----
###python实现的多线程爬虫 【代码质量规范性高】
	根据配置文件来完成爬取web内容
```python
程序运行:
python mini_spider.py -c spider.conf		

配置文件spider.conf:			

[spider]				
url_list_file: ./urls ; 种子文件路径		
output_directory: ./output ; 抓取结果存储目录
max_depth: 1 ; 最大抓取深度(种子为0级)		
crawl_interval: 1 ; 抓取间隔. 单位: 秒   
crawl_timeout: 1 ; 抓取超时. 单位: 秒   
target_url: .*.(htm|html)$ ; 需要存储的目标网页URL pattern(正则表达式)   
thread_count: 8 ; 抓取线程数
```   
-----------------

### other
程序需要依赖的模块  
+ beautifulsoup4 
