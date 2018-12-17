简介：
抓取Zolo网站Market Stats页面的相关信息

环境python3.6

运行条件：
    1：项目根目录下的tools文件夹下需要一个"城市文件列表"必须是csv文件的格式
    2：命名必须是"SourceData"
    3:字段名称必须是"City"

运行项目
    1：切换到项目根目录ZoloProject
    键入命令pip install -r requirement.txt
    2: python main.py 
    
    
其他：
    1：项目的配置文件在项目更目录下Zolo文件夹下
        1：数据库的连接配置
        2：数据完成抓取后的基本字段插入和省份code获取语句；
    2：关于其他sql语句则在ZoloProject/Zolo/pipelines的close_spider函数中
        如果你想修改最后的省份插入和国家插入语句，只需替换到相应的字符串即可
    
    
    
    

