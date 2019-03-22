import datetime
import psycopg2
import requests
import json


def create_tables():
    """创建数据库表
    """
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()

    # 创建天气数据表
    sql = """CREATE TABLE weather_real(create_at timestamp,
                                date date,
                                publishTime timestamp,
                                city varchar,
                                temperature float,
                                humidity float,
                                pressure float,
                                windDirection varchar,
                                windSpeed float,
                                windPower varchar,
                                info varchar,
                                img varchar,
                                rain float,        
                                feelst float,
                                rcomfort varchar,
                                icomfort varchar,
                                aq varchar,
                                aqi varchar,
                                aqiCode varchar,
                                aq_text varchar);"""
    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()


def get_data(url):
    response = requests.get(url)
    try:
        content = response.content.decode("utf-8")
        data = json.loads(content)
    except Exception:
        data = {}
    return data


def get_cities(province_code):
    """获取所有城市
    """
    url = "http://www.nmc.cn/f/rest/province/{}".format(province_code)
    cities_data = get_data(url)
    return cities_data


def get_weather_real(city_code):
    """实时天气数据
    """
    url = "http://www.nmc.cn/f/rest/real/{}".format(city_code)
    response = requests.get(url, params={"_": "1552990871892"})
    try:
        content = response.content.decode("utf-8")
        data = json.loads(content)
    except Exception:
        data = {}

    if not data:
        return {}

    weather_data = {
        "publishTime": data["publish_time"],
        "city": data["station"]["code"],
        "temperature": data["weather"]["temperature"],
        "humidity": data["weather"]["humidity"],
        "pressure": data["weather"]["airpressure"],
        "windDirection": data["wind"]["direct"],
        "windSpeed": data["wind"]["speed"],
        "windPower": data["wind"]["power"],
        "info": data["weather"]["info"],
        "img": data["weather"]["img"],
        "rain": data["weather"]["rain"],
        "feelst": data["weather"]["feelst"],
        "rcomfort": data["weather"]["rcomfort"],
        "icomfort": data["weather"]["icomfort"],
    }
    return weather_data


def get_aqi(city_code):
    """获取空气质量
    """
    url = "http://www.nmc.cn/f/rest/aqi/{}".format(city_code)
    response = requests.get(url, params={"_": "1552990871892"})
    try:
        content = response.content.decode("utf-8")
        data = json.loads(content)
    except Exception:
        data = {}

    aqi_data = {
        "aq": data.get("aq", 9999),
        "aqi": data.get("aqi", 9999),
        "aqiCode": data.get("aqiCode", "-"),
        "aq_text": data.get("text", "-")
    }
    return aqi_data


def main():
    # 连接数据库
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()

    # 省份
    cur.execute("SELECT * FROM areas;")
    provinces = cur.fetchall()

    for province in provinces:
        # 城市
        cities = get_cities(province[0])
        for city in cities:
            weather_data = get_weather_real(city["code"])
            aqi_data = get_aqi(city["code"])

            if weather_data and aqi_data:
                create_at = datetime.datetime.now()
                date = weather_data["publishTime"].split(" ")[0]

                sql = "INSERT INTO weather_real values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                cur.execute(sql, (create_at,
                                  date,
                                  weather_data["publishTime"],
                                  city["code"],
                                  weather_data["temperature"],
                                  weather_data["humidity"],
                                  weather_data["pressure"],
                                  weather_data["windDirection"],
                                  weather_data["windSpeed"],
                                  weather_data["windPower"],
                                  weather_data["info"],
                                  weather_data["img"],
                                  weather_data["rain"],
                                  weather_data["feelst"],
                                  weather_data["rcomfort"],
                                  weather_data["icomfort"],
                                  aqi_data["aq"],
                                  aqi_data["aqi"],
                                  aqi_data["aqiCode"],
                                  aqi_data["aq_text"]
                                  ))
                conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    # create_tables()
    main()
