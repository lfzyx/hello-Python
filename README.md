# python-simpletool

**jscompress.py** 

js压缩工具，调用jsmin

`$python3 jscompress.py [js folder]`

----

**tomcat_logbak.py**

tomcat的日志归档工具，tomcat的log目录会产生大量日志文件，而且不知道如何关闭，所以只能先写个程序把日志归档

`$python3 tomcat_logbak.py [DIR tomcat0 tomcat1...]`

----

**deploy_tomcat.py**

tomcat的web工程有很多配置项目，该工具可以在生产环境部署时可以自动替换配置文件中的内容

`$python3 deploy_tomcat.py [deploy_tomcat.conf project tomcat0 tomcat1...]`