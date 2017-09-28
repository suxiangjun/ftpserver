## 项目名称：ftp工具

*本软件只在windows系统，python3环境下运行过，Linux的可能要做相应的修改。*

#### 实现功能

- 1.多用户同时登录
- 2.多用户上传/下载文件
- 3.不同用户家目录不同
- 4.用户查看当前目录下文件
- 5.全部使用面向对象知识

#### 程序架构

```php+HTML
├──ftp-client                # 客户端
│      └──client.py          #  ftp客户端执行程序     
│                   
│
├──ftp-server                #服务端
│      │──bin                       
│      │   ├──server.py      #  ftp服务端执行程序   
│      │   └──__init__.py
│      └──data               # 用户数据存储的地方
│      │    ├──password.bak  # 存所有用户的账户数据基本数据
│      │	├──password.dat
│      │    └──password.dir
│      │──home               # 用户家目录
│      └──log                # 日志目录
│          ├──ftp.log        # 用户登入和操作日志
│          └──__init__.py
│──README

```


`注意事项：`下载/上传的文件，和客户端程序所在目录相同

[博客地址]: http://www.cnblogs.com/xiangjun555

