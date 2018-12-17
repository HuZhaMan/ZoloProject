简介：

抓取Zolo网站Market Stats页面的相关信息

环境python3.6

运行条件：

1：项目根目录下的tools文件夹下需要一个"城市文件列表"必须是csv文件的格式

2：命名必须是"SourceData"

3:字段名称必须是"City"

运行项目
1：切换到项目根目录ZoloProject

2:键入命令pip3 install -r requirement.txt

3: python3 main.py 
    
    
其他：

1：项目的配置文件在项目更目录下Zolo文件夹下

2：数据库的连接配置

3：数据完成抓取后的基本字段插入和省份code获取语句；

4：关于其他sql语句则在ZoloProject/Zolo/pipelines的close_spider函数中
如果你想修改最后的省份插入和国家插入语句，只需替换到相应的字符串即可
    
ubuntu 16.04的环境配置方法
安装：

1、add-apt-repository ppa:jonathonf/python-3.6

2、apt-get update

3、apt-get install python3.6

配置只输入python3时就默认使用3.6版本：

1、update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1

2、update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2

3、update-alternatives --config python3

4、python3 -V

设置pip:

1、apt-get install python3-pip　　　　# Python3

如果出现：ModuleNotFoundError: No module named 'gdbm' 这个错误，执行：

sudo apt-get install python3.6-gdbm

可以直接通过：git clone https://github.com/LIDD-UP/ZoloProject 

将项目克隆到本地

通过pip3 install -r requirement.txt可能出现的问题：

1：    distutils.errors.DistutilsError: Setup script exited with error: command 'x86_64-linux-gnu-gcc' failed with exit status 1

解决办法：sudo apt-get install python3.6-dev

还没有解决就看这篇blog：

https://stackoverflow.com/questions/26053982/setup-script-exited-with-error-command-x86-64-linux-gnu-gcc-failed-with-exit
    

