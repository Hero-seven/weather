#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

import requests
import pprint
import csv

from lxml import etree
from weather.settings import BASE_DIR


def get_city_url_list():
    """获取全国所有城市"""
    # 获取所有省份
    url = "http://weather.sina.com.cn/beijing"
    response = requests.get(url)
    content = response.content.decode("utf-8")
    # pprint.pprint(content)
    # 提取数据
    # 获取根元素对象
    eroot = etree.HTML(content)
    # 获取所有省份url
    province_list = eroot.xpath("// div[ @class ='wnbc_piC']/a/@href")
    province_url_list = [province for province in province_list]
    # pprint.pprint(province_url_list)

    city_url_list = []
    # 获取各省份的县/区url
    for province_url in province_url_list:
        response = requests.get(province_url)
        content = response.content.decode("utf-8")
        # 获取根元素对象
        eroot = etree.HTML(content)
        # 获取所有县/区url
        the_province_citys = eroot.xpath("//div[@class='wd_cmc']//td[@style='width:136px;']/a/@href")
        pprint.pprint(the_province_citys)
        city_url_list.extend(the_province_citys)
    print(len(city_url_list))
    return city_url_list


def get_precipitation_data(url_data):
    """获取某个城市降水量信息"""
    # 获取网页内容
    response = requests.get(url_data["district_url"])
    content = response.content.decode("utf-8")
    # pprint.pprint(content)
    # 提取数据
    # 获取根元素对象
    eroot = etree.HTML(content)
    # 获取降水量数据列表
    str_list = eroot.xpath("//span[@class='blk6_i_res']/text()")
    data_real = [float(str[0:-2]) for str in str_list]
    # 添加城市信息
    data = [url_data["province_name"], url_data["city_name"], url_data["district_name"]]
    data.extend(data_real)
    print(data)
    return data


def get_temperature_list(url_data):
    """获取某个城市的气温"""
    # 获取网页内容
    response = requests.get(url_data["district_url"])
    content = response.content.decode("utf-8")
    # pprint.pprint(content)
    # 提取数据
    # 获取根元素对象
    eroot = etree.HTML(content)
    # 获取气温数据列表
    str_list = eroot.xpath("//div[@class ='blk6_c0_1']/@data-daymthtemp")
    data_list = str_list[0].split(",")
    data_real = [float(data) for data in data_list if data]
    # 添加城市信息
    data = [url_data["province_name"], url_data["city_name"], url_data["district_name"]]
    data.extend(data_real)
    print(data)
    return data


def save_precipitation_data(url_data_list):
    # 保存数据至csv文件
    with open("./data/precipitation.csv", "w", newline="", encoding='utf-8') as f:
        f_csv = csv.writer(f, dialect="excel")
        # 写入表头
        row = ["province", "city", "district", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct",
               "Nov", "Dec"]
        f_csv.writerow(row)

        for url_data in url_data_list:
            # 获取降水量数据
            data = get_precipitation_data(url_data)
            # 写入数据
            f_csv.writerow(data)


def save_temperature_data(url_data_list):
    # 保存数据至csv文件
    with open("./data/temperature.csv", "w", newline="", encoding='utf-8') as f:
        f_csv = csv.writer(f, dialect="excel")
        # 写入表头
        row = ["province", "city", "district", "city", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept",
               "Oct", "Nov", "Dec"]
        f_csv.writerow(row)

        for url_data in url_data_list:
            # 获取气温数据
            data = get_temperature_list(url_data)
            # 写入数据
            f_csv.writerow(data)


def main():
    # 获取所有城市信息
    file_path = os.path.join(os.path.dirname(BASE_DIR), 'utils/data/areas.csv')
    url_data_list = []
    with open(file_path) as f:
        data_list = csv.reader(f)
        for data in data_list:
            url_data = {
                "province_name": data[0],
                "city_name": data[1],
                "district_name": data[2],
                "district_url": data[3]
            }
            pprint.pprint(url_data)
            url_data_list.append(url_data)

    url_data_list = url_data_list[1:]


    # 获取降水量数据并保存至csv文件
    save_precipitation_data(url_data_list)


    # 获取气温数据并保存至csv文件
    save_temperature_data(url_data_list)


if __name__ == '__main__':
    main()
