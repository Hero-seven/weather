# 获取逐3小时天气数据
from pprint import pprint

import requests
from django.utils import timezone
from lxml import etree


# url = "http://www.nmc.cn/publish/forecast/ASC/guangan.html"
# xpath = "//div[@id='hour3']/div[@id='day0']/div[@class='row first']/div[@style='font-size: 12px;']"


# 获取省份的值
# "//div[@class='cityselect']//select[@id='provinceSel']/option/@value"
# "//div[@class='cityselect']//select[@id='provinceSel']/option/text()"


def get_province():
    """获取省份信息
    """
    url = "http://www.nmc.cn/publish/forecast/ABJ/beijing.html"
    response = requests.get(url)
    content = response.content.decode("utf-8")
    # pprint(content)

    # 提取数据
    eroot = etree.HTML(content)
    # print(eroot)

    province_name_list = eroot.xpath(
        "//div[@class='cityselect']//select[@id='provinceSel']/option[@value='ABJ']/text()")
    province_value_list = eroot.xpath("//div[@class='cityselect']//select[@id='provinceSel']/option/text()")

    print('省份列表:', province_name_list)
    for i in range(len(province_name_list)):
        print(province_name_list[i], province_value_list[i])


def get_html():
    """获取网页内容
    """
    url = "http://www.nmc.cn/publish/forecast/ABJ/beijing.html"
    response = requests.get(url)
    content = response.content.decode("utf-8")
    eroot = etree.HTML(content)
    return eroot


def get_date(eroot):
    """获取日期
    """
    date_list = eroot.xpath("//div[@class='btitle']/span/text()")
    date = date_list[0][4:14]
    print(date)
    return date


def get_times(eroot):
    """获取时间
    """
    data = eroot.xpath(
        "//div[@id='hour3']/div[@id='day0']/div[@class='row first']/div[@style='font-size: 12px;']/text()")
    time_list = [str.split("\n")[1][-5:] for str in data]
    print(time_list)
    return time_list


def get_phenomenon(eroot):
    """获取天气现象
    """
    phenomena_list = eroot.xpath("//div[@id='hour3']/div[@id='day0']/div[@class='row second tqxx']//img/@src")
    print(phenomena_list)
    return phenomena_list


def get_temperature(eroot):
    """获取气温
    """
    data = eroot.xpath("//div[@id='hour3']/div[@id='day0']/div[@class='row wd']/div/text()")
    temperature = [str.split('\n')[1][:-2].lstrip() for str in data][1:]
    temperature_list = [float(x) for x in temperature]
    print(temperature_list)
    return temperature_list


def get_precipitation(eroot):
    """获取降水量
    """
    data = eroot.xpath("//div[@id='hour3']/div[@id='day0']/div[@class='row js']/div/text()")
    precipitation = [str.split('\n')[1].strip() for str in data][1:]
    precipitation_list = [0 if data == "无降水" else float(data[:-2]) for data in precipitation]
    print(precipitation_list)
    return precipitation_list


def get_wind_speed(eroot):
    """获取风速
    """
    data = eroot.xpath("//div[@id='hour3']/div[@id='day0']/div[@class='row winds']/div/text()")
    winds = [str.split('\n')[1].strip()[:-3] for str in data][1:]
    wind_speed_list = [float(data) for data in winds]
    print(wind_speed_list)
    return wind_speed_list


def get_wind_direction(eroot):
    """获取风向
    """
    data = eroot.xpath("//div[@id='hour3']/div[@id='day0']/div[@class='row windd']/div/text()")
    wind_direction_list = [str.split('\n')[1].strip() for str in data][1:]
    print(wind_direction_list)
    return wind_direction_list


def get_pressure(eroot):
    """获取气压
    """
    data = eroot.xpath("//div[@id='hour3']/div[@id='day0']/div[@class='row qy']/div/text()")
    pressure = [str.split('\n')[1].strip()[:-3] for str in data][1:]
    pressure_list = [float(x) for x in pressure]
    print(pressure_list)
    return pressure_list


def get_rh(eroot):
    """获取相对湿度
    """
    data = eroot.xpath("//div[@id='hour3']/div[@id='day0']/div[@class='row xdsd']/div/text()")
    rh = [str.split('\n')[1].strip()[:-1] for str in data][1:]
    rh_list = [round(float(x) / 100, 3) for x in rh]
    print(rh_list)
    return rh_list


def get_cloud(eroot):
    """获取云量
    """
    data = eroot.xpath("//div[@id='hour3']/div[@id='day0']/div[@class='row yl']/div/text()")
    cloud = [str.split('\n')[1].strip()[:-1] for str in data][1:]
    cloud_list = [round(float(x) / 100, 3) for x in cloud]
    print(cloud_list)
    return cloud_list


def get_visibility(eroot):
    """获取能见度
    """
    data = eroot.xpath("//div[@id='hour3']/div[@id='day0']/div[@class='row njd']/div/text()")
    visibility_list = [str.split('\n')[1].strip() for str in data][1:]
    # visibility_list = [round(float(data) / 100, 3) for data in visibility]
    print(visibility_list)
    return visibility_list


def get_weather_hour3():
    """获取逐三小时天气实况
    """
    # 获取网页内容
    eroot = get_html()

    # 提取数据：
    # 日期
    date = get_date(eroot)
    # 时间
    time_list = get_times(eroot)
    # 天气现象
    phenomena_list = get_phenomenon(eroot)
    # 气温
    temperature_list = get_temperature(eroot)
    # 降水
    precipitation_list = get_precipitation(eroot)
    # 风速
    wind_speed_list = get_wind_speed(eroot)
    # 风向
    wind_direction_list = get_wind_direction(eroot)
    # 气压
    pressure_list = get_pressure(eroot)
    # 相对湿度
    rh_list = get_rh(eroot)
    # 云量
    cloud_list = get_cloud(eroot)
    # 能见度
    visibility_list = get_visibility(eroot)

    for i in range(len(time_list)):
        date = date
        time = time_list[i]
        phenomena = phenomena_list[i]
        temperature = temperature_list[i]
        precipitation = precipitation_list[i]
        wind_speed = wind_speed_list[i]
        wind_direction = wind_direction_list[i]
        pressure = pressure_list[i]
        rh = rh_list[i]
        cloud = cloud_list[i]
        visibility = visibility_list[i]


if __name__ == '__main__':
    # get_province()
    get_weather_hour3()
