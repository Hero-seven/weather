#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import pprint
import csv

from lxml import etree


def get_city_data():
    """获取全国所有城市"""
    with open("areas.csv", "w", newline="", encoding='utf-8') as f:
        f_csv = csv.writer(f, dialect="excel")
        # 写入表头
        row = ["province", "city", "district"]
        f_csv.writerow(row)

        # 获取所有省份
        url = "http://weather.sina.com.cn/beijing"
        response = requests.get(url)
        content = response.content.decode("utf-8")
        # pprint.pprint(content)
        # 提取数据
        # 获取根元素对象
        eroot = etree.HTML(content)

        data = []
        # 获取所有省份url及名称
        province_a_list = eroot.xpath("//div[@class ='wnbc_piC']/a")
        province_list = []

        for a in province_a_list:
            # 获取省级url和名称
            province_url = a.xpath("@href")[0]
            province_name = a.xpath("text()")[0]
            print(province_name)
            province = {
                "province_name": province_name,
                "province_url": province_url
            }
            province_list.append(province)

            # 获取该省市级url和名称
            response = requests.get(province_url)
            content = response.content.decode("utf-8")
            # 获取根元素对象
            eroot = etree.HTML(content)

            city_a_list = eroot.xpath("//div[@class='wd_cmain']")
            for a in city_a_list:
                # 获取省级url和名称
                city_name = a.xpath("div[@class='wd_cmh']/text()")[0].split("\n")[1][20:]
                print(repr(city_name))
                district_url_list = a.xpath("div[@class='wd_cmc']//td[@style='width:136px;']/a/@href")

                # 获取县/区及url及名称
                for district_url in district_url_list:
                    # 获取该省市级url和名称
                    response = requests.get(district_url)
                    content = response.content.decode("utf-8")
                    # 获取根元素对象
                    eroot = etree.HTML(content)

                    district_name = eroot.xpath("//h4[@class='slider_ct_name']/text()")[0]
                    print(district_name)

                    csv_data = [province_name, city_name, district_name, district_url]
                    f_csv.writerow(csv_data)


if __name__ == '__main__':
    get_city_data()
