# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: process_city_list.py
@time: 2018/11/14
"""
import pandas as pd
import re


def realize_capitalize(source_str):
    return source_str.capitalize()


def generate_province_city_map_file(data):
    data = data[['City', 'Province']]
    data['City'] = [x.replace('-', ' ') for x in data['City']]
    data['City'] = ['_'.join(x.split(' ')) for x in data['City']]
    data['City'] = ['_'.join(list(map(realize_capitalize, x.split('_')))) for x in data['City']]
    data['City'] = [' '.join(list(map(realize_capitalize, x.split('_')))) for x in data['City']]
    data.to_csv('./province_city_map.csv', index=False)


class ProcessCityList():
    def process_city_list(self,data):
        data = data['City']
        data = data.dropna()
        data = list(data)
        data = pd.DataFrame(data, columns=['city'])

        # 其实url是从Toronto开始的；
        data =data[data.city !='Toronto']

        # 这里不需要小写也可以做到
        # data['city'] = data['city'].str.lower()
        # 将首字母大写
        # 定义一个首字母大写函数
        def realize_capitalize(source_str):
             return source_str.capitalize()

        data['city'] = [x.replace('-', ' ') for x in data['city']]
        data['city'] = ['_'.join(x.split(' ')) for x in data['city']]
        data['city'] = ['_'.join(list(map(realize_capitalize, x.split('_')))) for x in data['city']]
        # data['city'] = [x.replace('-','_') for x in data['city']]
        # data_list_new = list(data['city'])
        # 非字符的方式去掉一些特殊的字符；经过测试出现特殊字符网址就错误，但是如果只要是字符都不会出错；
        data_list_new = [x for x in data['city'] if len(re.findall(r'\W', x)) == 0]
        print('data_list_new',data_list_new)
        data_list_new = [x.replace('_', '-') for x in data_list_new]
        data_list_new = ['https://www.zolo.ca/{}-real-estate/trends'.format(x) for x in data_list_new]

        new_data = pd.DataFrame(data_list_new,columns=['city'])

        new_data.to_csv('./DataAfterProcess.csv',index=False)
        # return new_data


if __name__ == '__main__':
    data = pd.read_csv('./SourceData.csv')
    # print(data.shape)
    pcl = ProcessCityList()
    new_data = pcl.process_city_list(data)
    # new_data.to_csv('./city.csv',index=False)
    # print(new_data.head())
    # print(new_data.shape)
    # ProcessCityList(data)





'''
对于有斜杠的需要去除；而且有可能是不正确的;

'''