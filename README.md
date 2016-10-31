#
1.	安装系统
目前支持centos7, windows系统<不需要编译rpm,直接运行源码>等
2.	安装python环境
Centos自带python，不需要安装
Windows系统，需要下载python2.7版本的二进制文件进行安装
3.	编译rpm
将源代码复制到系统，解压之后，打开终端，切换到源代码目录，执行 python setup.py bdist_rpm 会产生dist目录，下面有oc-service-0.0.1-1.noarch.rpm。
4.	安装rpm
运行命令rpm –ivh oc-service-0.0.1-1.noarch.rpm。
5.	启动服务
systemctl start oc-service
或者执行
cd /usr/lib/python2.7/site-packages/oc
python oc_service.py
6.	命令行设置数据
oc_utils add test 123456   //添加数据
oc_utils update test 654321//更新数据
oc_utils query  test       //查询数据
oc_utils delete test 123456    //删除数据
oc_utils list              //列出所有数据
7.	接受远程调用
目前支持远程调用的方法有：
add_data_to_cache
update_data_to_cache
delete_data_from_cache
query_data_from_cache
query_all_data_from_cache
8.	数据持久化
/usr/lib/python2.7/site-packages/oc/cache.db是持久化数据， 重启机器后，会再次加载以前的数据。新增加数据之后，会自动添加到数据库里面，进行持久化保存。

{"jsonrpc":"2.0", "method":"add_data_to_cache","id":"test",'params':{'key':"aaa",'value':"111"}} 
