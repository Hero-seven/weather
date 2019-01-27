#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import pprint
import matplotlib.pyplot as plt
import csv
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

from lxml import etree


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
    print(city_name)
    # 添加城市信息
    data.insert(0, city_name[0])
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
    print(city_name)
    # 添加城市信息
    data.insert(0, city_name[0])
    print(data)
    return data


def save_precipitation_data():
    # 保存数据至csv文件
    with open("./precipitation.csv", "w", newline="", encoding='utf-8') as f:
        f_csv = csv.writer(f, dialect="excel")
        # 写入表头
        row = ["city", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        f_csv.writerow(row)

        # 循环遍历所有城市降水量数据
        city_url_list = get_city_url_list()
        for city_url in city_url_list:
            # 获取降水量数据
            data = get_precipitation_data(city_url)
            # 写入数据
            f_csv.writerow(data)


def save_temperature_data():
    # 保存数据至csv文件
    with open("./temperature.csv", "w", newline="", encoding='utf-8') as f:
        f_csv = csv.writer(f, dialect="excel")
        # 写入表头
        row = ["city", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        f_csv.writerow(row)

        # 循环遍历所有城市降水量数据
        city_url_list = get_city_url_list()
        for city_url in city_url_list:
            # 获取气温数据
            data = get_temperature_list(city_url)
            # 写入数据
            f_csv.writerow(data)


def make_chart():
    """绘制图表"""
    # 1.准备数据
    # 电影名称
    # 横坐标
    # months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    months = ["{}月".format(i) for i in range(1, 13)]
    print(months)
    x = range(len(months))
    # 票房数据
    y = data[1:]

    # 2.创建画布
    plt.figure(figsize=(20, 8), dpi=100)

    # 3.绘制图像
    plt.bar(x, y, width=0.5)

    # 5.修改横坐标刻度信息
    plt.xticks(x, months)

    # 6.添加坐标轴信息及标题
    plt.xlabel("月份")
    plt.ylabel("降水量")
    plt.title("2018年全年降水量")

    # 7.显示网格
    # plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig("./graphes/北京.png")

    # 4.显示图像
    plt.show()
    pass


def main():
    # 获取降水量数据并保存至csv文件
    # save_precipitation_data()

    # 获取气温数据并保存至csv文件
    save_temperature_data()

    # 获取全国所有城市信息
    # get_city_url_list()


if __name__ == '__main__':
    main()
