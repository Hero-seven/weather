import requests
import json
from pprint import pprint

from weather_hour.models import City, WeatherHour


def get_data(url):
    response = requests.get(url)
    try:
        content = response.content.decode("utf-8")
        data = json.loads(content)
    except Exception:
        data = {}
    return data


def get_provinces():
    """获取省份
    """
    url = "http://www.nmc.cn/f/rest/province"
    provinces_data = get_data(url)
    # pprint(provinces_data)

    return provinces_data


def get_citys(province_code):
    """获取所有城市
    """
    url = "http://www.nmc.cn/f/rest/province/{}".format(province_code)
    citys_data = get_data(url)
    return citys_data


def save_citys():
    """保存城市信息'
    """
    provinces_data = get_provinces()
    for province in provinces_data:
        province_code = province["code"]
        province = City.objects.create(**province)
        citys_data = get_citys(province_code)
        for city in citys_data:
            city_data = {
                "code": city["code"],
                "name": city["city"],
                "url": city["url"],
                "parent": province
            }
            City.objects.create(**city_data)


def get_weather_hour(city_code):
    """获取逐小时天气实况
    """
    url = "http://www.nmc.cn/f/rest/passed/{}".format(city_code)
    weather_data = get_data(url)
    return weather_data


def get_weather():
    """获取并保存数据
    """
    # 省份
    provinces = City.objects.filter(parent=None)
    for province in provinces[:1]:
        # 城市
        citys = get_citys(province.code)
        for city in citys:
            weather_data = get_weather_hour(city["code"])
            pprint(weather_data)
            # 保存某城市天气数据
            for data in weather_data:
                date = data["time"].split(" ")[0]
                WeatherHour.objects.create(**data, date=date, city_id=city["code"])
