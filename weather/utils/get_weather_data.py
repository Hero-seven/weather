#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import pprint
import csv

from lxml import etree

from utils.get_city_data import get_city_data


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


def get_precipitation_data(city_url):
    """获取某个城市降水量信息"""
    # 获取网页内容
    response = requests.get(city_url)
    content = response.content.decode("utf-8")
    # pprint.pprint(content)
    # 提取数据
    # 获取根元素对象
    eroot = etree.HTML(content)
    # 获取降水量数据列表
    str_list = eroot.xpath("//span[@class='blk6_i_res']/text()")
    data = [float(str[0:-2]) for str in str_list]
    city_name = eroot.xpath("//h4[@class='slider_ct_name']/text()")
    # 添加城市信息
    data.insert(0, city_name[0])
    print(data)
    return data


def get_temperature_list(city_url):
    """获取某个城市的气温"""
    # 获取网页内容
    response = requests.get(city_url)
    content = response.content.decode("utf-8")
    # pprint.pprint(content)
    # 提取数据
    # 获取根元素对象
    eroot = etree.HTML(content)
    # 获取气温数据列表
    str_list = eroot.xpath("//div[@class ='blk6_c0_1']/@data-daymthtemp")
    data_list = str_list[0].split(",")
    data = [float(data) for data in data_list if data]
    city_name = eroot.xpath("//h4[@class='slider_ct_name']/text()")
    # 添加城市信息
    data.insert(0, city_name[0])
    print(data)
    return data


def save_precipitation_data(city_url_list):
    # 保存数据至csv文件
    with open("./data/precipitation.csv", "w", newline="", encoding='utf-8') as f:
        f_csv = csv.writer(f, dialect="excel")
        # 写入表头
        row = ["city", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        f_csv.writerow(row)

        # 循环遍历所有城市降水量数据
        for city_url in city_url_list:
            # 获取降水量数据
            data = get_precipitation_data(city_url)
            # 写入数据
            f_csv.writerow(data)


def save_temperature_data(city_url_list):
    # 保存数据至csv文件
    with open("./data/temperature.csv", "w", newline="", encoding='utf-8') as f:
        f_csv = csv.writer(f, dialect="excel")
        # 写入表头
        row = ["city", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        f_csv.writerow(row)

        # 循环遍历所有城市降水量数据
        for city_url in city_url_list:
            # 获取气温数据
            data = get_temperature_list(city_url)
            # 写入数据
            f_csv.writerow(data)


def main():
    # 获取所有城市列表
    url_data_list = get_city_data()

    for url_data in url_data_list:
        print(url_data["province_name"])
        print(url_data["city_name"])
        print(url_data["district_name"])
        print(url_data["district_url"])


        # 获取降水量数据并保存至csv文件
        save_precipitation_data(url_data)

        # 获取气温数据并保存至csv文件
        save_temperature_data(url_data)


if __name__ == '__main__':
    main()
