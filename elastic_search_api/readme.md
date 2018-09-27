# Discription

包含：	增加索引、更新索引
		call_id查询、dialog_id查询、session_id查询、topic查询、静默时间查询、
		时间范围查询、interruption查询、文本单句搜索、文本多句搜索、
		文本复杂逻辑精准搜索、话术分析器查询、文本分析器查询

# Requirements
- python3
- elasticsearch

# Enviroments
### 1.操作系统：linux14.04
### 2.java环境
查看java -version
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/1.jpg)
若没有Java环境，需进行配置，命令如下：

```
	sudo add-apt-repository ppa:webupd8team/java
	sudo apt-get update
	sudo apt-get install oracle-java8-installer
	sudo apt-get install oracle-java8-set-default
```

配置成功后查看java -version，应显示配置完成
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/2.jpg)
切换到用户目录中，新建java 文件 vim Helloworld.java
然后敲入如下代码进行测试：
	class HelloWorld
	{
		public static void main(String args[])
		{
			System.out.println('hello world');
		}
	}
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/3.jpg)
javac 编译文件 javac Helloworld.java 生成HelloWorld.class文件,命令为：
	javac Helloworld.java
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/4.jpg)
运行Java 程序 java Helloworld,可以看出程序运行成功，java 环境配置没问题。
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/5.jpg)
### 3.Elasticsearch 环境部署安装
在Elasticsearch官网下载对应的版本,即6.4.1版本
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/6.jpg)
下载后解压文件：
	sudo tar -zxvf elasticsearch-6.4.1.tar.gz
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/7.jpg)
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/8.jpg)
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/9.jpg)	
解压以后切换到elasticsearch对应的文件目录下 ./bin/elasticsearch启动搜索引擎
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/10.jpg)
查看节点状态:
	
	curl localhost:9200/_cat/health?v
	
如所示，ES节点已经成功启动	
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/11.jpg)	
若ES启动权限不够，需手动提升权限：	
	（示例）sudo chown caralette /tmp/mozilla_caralette0/elasticsearch-6.4.1() -R		
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/12.jpg)
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/13.jpg)	
启动信息里有一个关于绑定ip的描述：
	'bound_addresses{[::1]:9200},{120.0.0.1:9200}'		
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/14.jpg)	
在浏览器中输入地址，可以实现外网访问	
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/15.jpg)
	
### 4.Kibana的配置
Kibana 是基于Elasticsearch做的一个搜索结果可视化插件
在官网找到对应版本下载:6.4.1	
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/16.jpg)
解压压缩包:
	tar zxvf kibana-6.4.1-linux-x86_64.tar.gz		
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/17.jpg)	
解压以后在bin目录下启动kibana	
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/18.jpg)	
在启动信息里找到端口号	
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/19.jpg)	
在浏览器中访问 localhost：5601	
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/20.jpg)	
应当可以使用	
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/21.jpg)
![](https://github.com/xiezongai/Sentinel-Pris/raw/master/elastic_search_api/img/22.jpg)




