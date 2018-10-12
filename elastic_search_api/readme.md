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

![](./img/1.jpg)

若没有Java环境，需进行配置，命令如下：

```
	sudo add-apt-repository ppa:webupd8team/java
	sudo apt-get update
	sudo apt-get install oracle-java8-installer
	sudo apt-get install oracle-java8-set-default
```

配置成功后查看java -version，应显示配置完成

![](./img/2.jpg)



### 3.Elasticsearch 环境部署安装
在Elasticsearch官网下载对应的版本,即6.4.1版本

![](./img/6.jpg)

下载后解压文件：
```
	sudo tar -zxvf elasticsearch-6.4.1.tar.gz
```

![](./img/7.jpg)
![](./img/8.jpg)
![](./img/9.jpg)	

解压以后切换到elasticsearch对应的文件目录下 ./bin/elasticsearch启动搜索引擎

![](./img/10.jpg)

查看节点状态:
	```
	curl localhost:9200/_cat/health?v
	```
如所示，ES节点已经成功启动	

![](./img/11.jpg)

若ES启动权限不够，需手动提升权限：	
```
	（示例）sudo chown caralette /tmp/mozilla_caralette0/elasticsearch-6.4.1() -R
```
![](./img/12.jpg)
![](./img/13.jpg)

修改配置文件：
```
vim config/elasticsearch.yml
network.host: 0.0.0.0
```
重新启动es之后，应当能实现外网访问：
```
curl http://10.112.57.93:9200/
(ip应被替换，端口通常为9200不变)
```

![](./img/23.jpg)

如上则配置成功
	





