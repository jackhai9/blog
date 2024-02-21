## 环境搭建

1. 基于xampp来搭建Apache/Mysql/PHP环境，xampp版本为：xampp-linux-x64-7.1.9-0-installer.run ；

2. Mediawiki的版本为：mediawiki-1.29.1.tar.gz ；

## 安装过程

参考：https://www.mediawiki.org/wiki/Manual:Installing_MediaWiki_on_XAMPP

最终目录：

1. xampp安装目录： /opt/lampp

2. wiki的部署目录：/opt/lampp/htdocs/wiki

## 注意事项


1. 在最后安装Mediawiki的时候，因为远程服务器上没有桌面环境，也没有浏览器，所以无法通过本机windows上的浏览器直接ip访问来进行安装：ip是http://172.20.XXX.XXX/wiki ，到后面配置mysql时一直连不上数据库，估计跟ip访问有关 ：

   解决方法：在远程服务器通过lynx来模拟浏览器，安装lynx，（yum install lynx），使用方法是：`# lynx http://localhost/wiki/mw-config/index.php?page=Language`  开始进行安装，最后也下载到了LocalSettings.php 。

2. 把LocalSettings.php放到 /opt/lampp/htdocs/wiki目录下 。最好备份下LocalSettings.php.bak，后续会修改此文件，防止改坏。

## 配置说明

wiki部署服务器：172.20.XXX.XXX，端口321，用户YYY

1. 172.20.XXX.XXX之前已经有了mysql，wiki使用了单独的mysql，端口是10086   数据库：/opt/lampp/var/mysql/my_wiki

2. 命令行连接数据库：# /opt/lampp/bin/mysql -uroot -p  【密码：mysql的root用户的密码】

3. 默认访问http://172.20.XXX.XXX/phpmyadmin/是免密登录的，如下配置/opt/lampp/phpmyadmin/config.inc.php关闭免密登录：

     ```php
     $cfg['Servers'][$i]['auth_type'] = 'cookie';
     $cfg['Servers'][$i]['AllowNoPassword'] = false;
     ```

4. 可进行语言、上传文件等其他功能设置。默认"上传文件"功能未开启，现已开启并配置了支持更多文件类型

5. <s>目前未对数据库做定时备份，以后数据多起来，需要定时备份。历史备份：/opt/lampp/bin/mysqldump -uroot -p my_wiki > /data/wiki_mysql_back/my_wiki_backup20180705.sql</s>
[现已定时备份](#数据库备份)

6. 设置了对匿名用户隐藏如下部分：

     * 隐藏工具栏Toolbox： skins/Vector/VectorTemplate.php
     
       ```php
       case 'TOOLBOX':
       if ( $this->data['loggedin'] ) {
           $this->renderPortal( 'tb', $this->getToolbox(), 'toolbox', 'SkinTemplateToolboxEnd' );
       }
       ```
       
     * 隐藏查看源码（View source）和查看历史（View history）： skins/Vector/VectorTemplate.php
     
       ```php
       if ( !($this->data['loggedin'])||count( $this->data['view_urls'] ) == 0 ) {
           echo ' emptyPortlet';
       }
       ```

7. 启用WikiEditor。MediaWiki自带的编辑器比较简单，用于页面编辑不太方便。从1.18版开始，MediaWiki中集成了一款增强型编辑器WikiEditor。

8. 启用语法高亮。MediaWiki默认集成了GeSHi(Generic Syntax Highlighter)插件，这是一款支持语法高亮显示的插件。

9. 首字母不再强制大写。

10. 安装了扩展 Extension:Contribution_Scores ，用来统计贡献者得分 [链接](https://www.mediawiki.org/wiki/Extension:Contribution_Scores)

11. 修改了时区LocalSettings.php：

    ```php
    $wgLocaltimezone="Asia/Shanghai";
    ```

12. Mediawiki默认的搜索search不好用，尤其是不支持中文。安装了扩展 Extension:CirrusSearch [链接](https://www.mediawiki.org/wiki/Extension:CirrusSearch) [链接](https://github.com/wikimedia/mediawiki-extensions-CirrusSearch)  
    
    需要先手动安装以下依赖：Elastica，Composer，JDK8，Elasticsearch。【注意：php命令的路径为：/opt/lampp/bin/php】
    
    > JDK8安装路径：/usr/local/jdk1.8.0_191
    >
    > Elasticsearch安装路径：/opt/elasticsearch-5.3.1，修改了启动脚本 ./bin/elasticsearch 里的 JAVA 变量：`JAVA="/usr/local/jdk1.8.0_191/bin/java"` ，指向JDK8
    >
    > Elasticsearch通过-d参数在后台运行。curl localhost:9200  测试es安装启动没问题。注意：不要以root用户启动es，可以es用户来启动。目前对es还没监控进行自动重启，后续可以加上。
    
13. 对外公开资料的目的：访问者不需要帐号就可以访问页面。访问者只能查看，不能修改。

      <font color="red">需要在服务器上追加配置：</font>

      wiki 服务器 ：172.20.XXX.XXX

      /opt/lampp/htdocs/wiki/LocalSettings.php  的  $wgWhitelistRead 变量中 新增资料名字（页面名字）即可：

      ```php
      # 例如，公开页面 “金蝶电子合同API对接文档”，“页面1”，“File:压缩文件2.zip”，。。。
      $wgWhitelistRead = array ("金蝶电子合同API对接文档","页面1","File:压缩文件2.zip");
      ```

      

## 常用命令


1. `/opt/lampp/lampp start`

2. `/opt/lampp/lampp stop`

3. `/opt/lampp/lampp restart`

## 服务监控


1. `crontab -e`

2. 脚本：/opt/monitor.sh

3. 日志：/var/log/cron.monitor.log

## 数据库备份

已经通过crontab定时备份wiki数据库： 

```bash
# /opt/mysql_bak.sh   wiki数据库定时备份,每天3点01分执行备份
01 3 * * * /opt/mysql_bak.sh >> /var/log/cron.mysql_bak.log 2>&1
```

其中 /opt/mysql_bak.sh 脚本内容如下：

```bash
/opt/lampp/bin/mysqldump -uroot my_wiki | gzip > /data/wiki_mysql_back/my_wiki_backup`date +%Y%m%d_%H%M%S`.sql.gz
# 删除1天之前的日志
find /data/wiki_mysql_back/ -type f -mtime +1 -exec rm {} \;
```

从压缩的备份文件直接恢复数据:

```bash
$ gunzip < /data/wiki_mysql_back/my_wiki_backup20180705.sql.gz | /opt/lampp/bin/mysql -uroot -p my_wiki
```

## es日志定期删除

已经通过crontab定期删除es日志： 

```bash
# /opt/es_log_clear.sh   
01 2 * * * /opt/es_log_clear.sh >> /var/log/cron.es_log_clear.log 2>&1
```

其中 /opt/es_log_clear.sh 脚本内容如下：

```bash
# 删除2天之前的日志
find /opt/elasticsearch-5.3.1/logs/ -type f -mtime +2 -exec rm {} \;
```

## 问题解决

一、mysql数据库改密码：

1. vim /opt/lampp/etc/my.cnf

[mysqld]

打开skiptable，即可无密码连接数据库。

2. 无密码连接数据库：mysql -uroot -p

   ```mysql
   >use mysql
   >update user set password=password("mysql的root用户的密码") where user="root";
   >flush privileges;
   >exit  
   ```

3. wiki配置文件LocalSettings.php里面的$wgDBpassword改为`mysql的root用户的密码`即可。

二、遇到Apache启动失败的问题是因为默认的80端口被占用，解决办法：

1.  修改/opt/lampp/etc/httpd.conf里的端口 Listen 80(修改为8011）

2.  修改/opt/lampp/etc/extra/httpd-ssl.conf里的443端口 Listen 443(修改为1443）

3.  /opt/lampp/lampp里的testport 80修改为testport 8011, testport 443修改为testport 1443

三、遇到访问受ip限制：

vim /opt/lampp/etc/extra/httpd-xampp.conf

注释掉：Require local

换成如下：

    Order allow,deny
    Allow from all
    Require all granted

四、目前没有对es进行自动重启，服务器如果重启过之后，es需要手动重启下。

方法：不要以root用户启动es，以es用户来启动：su es。Elasticsearch通过-d参数在后台运行（cd /opt/elasticsearch-5.3.1）：./bin/elasticsearch -d。然后 curl localhost:9200  测试es安装启动没问题。

五、页面下方出现如： <font color="red">/opt/lampp/htdocs/wiki/extensions/CirrusSearch/includes/Job/ElasticaWrite.php: Unsupported operand types Backtrace:</font> 的红色报错信息。

解决方法：检查es是否启动。 并执行命令：php /opt/lampp/htdocs/wiki/maintenance/runJobs.php 。 刷新页面即可。

六、搭建的lampp使用了默认的ftp账号密码，会有安全风险，需要修改。

解决方法：修改/opt/lampp/etc/proftpd.conf中的ftp账号daemon后面的密码，需要是密码加密后的形式。因为没有ftpasswd命令，所以使用了：`echo -n 'ftp密码' | openssl passwd -crypt -stdin`

最终：

ftp的账号：daemon

ftp的密码：ftp密码

ftp的密码-加密之后：ftp密码加密之后的密码

七、有时候数据库mysql重启会有问题，导致wiki页面访问报错：

Sorry! This site is experiencing technical difficulties.
Try waiting a few minutes and reloading.

(Cannot access the database)

问题原因：是mysql数据库问题，可能是user表损坏了。

解决方法：myisamchk -r /opt/lampp/var/mysql/mysql/user

最后：

```
/opt/lampp/lampp stopmysql
/opt/lampp/lampp startmysql
/opt/lampp/lampp status
```

  刷新页面即可。