import datetime
import requests
import json
import psycopg2


def create_tables():
    """创建数据库表
    """
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()

    # 创建城市表
    sql = """CREATE TABLE areas(code varchar(20) primary key not null,
                                    name varchar(20),
                                    url varchar(100),
                                    parent varchar(20)
                                    );"""
    cur.execute(sql)

    # 创建天气数据表
    sql = """CREATE TABLE weather(create_at timestamp,
                                date date,
                                time timestamp,
                                temperature float,
                                humidity float,
                                pressure float,
                                windDirection float,
                                windSpeed float,
                                rain1h float,
                                rain24h float,
                                rain12h float,
                                rain6h float,
                                city varchar
                                );"""
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


def get_provinces():
    """获取省份
    """
    url = "http://www.nmc.cn/f/rest/province"
    provinces_data = get_data(url)
    return provinces_data


def get_cities(province_code):
    """获取所有城市
    """
    url = "http://www.nmc.cn/f/rest/province/{}".format(province_code)
    cities_data = get_data(url)
    return cities_data


def save_areas():
    """保存城市信息'
    """
    # 连接数据库
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()
    provinces_data = get_provinces()
    for province in provinces_data:
        province_code = province["code"]
        province_name = province["name"]
        province_url = province["url"]

        sql = "INSERT INTO areas values (%s,%s,%s)"
        cur.execute(sql, (province_code, province_name, province_url))

        cities_data = get_cities(province_code)
        for city in cities_data:
            code = city["code"]
            name = city["city"]
            url = city["url"]
            parent = province_code

            sql = "INSERT INTO areas values (%s,%s,%s,%s)"
            cur.execute(sql, (code, name, url, parent))
            conn.commit()

    cur.close()
    conn.close()


def get_weather_hour(city_code):
    """获取逐小时天气实况
    """
    url = "http://www.nmc.cn/f/rest/passed/{}".format(city_code)

    weather_data = get_data(url)
    return weather_data


def get_weather():
    # 连接数据库
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()

    # 省份
    cur.execute("SELECT * FROM areas;")
    provinces = cur.fetchall()
    # print(provinces)

    for province in provinces:
        # 城市
        cities = get_cities(province[0])
        for city in cities:
            weather_data = get_weather_hour(city["code"])
            for data in weather_data:
                create_at = datetime.datetime.now()
                date = data["time"].split(" ")[0]

                sql = "INSERT INTO weather values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                cur.execute(sql, (create_at,
                                  date,
                                  data["time"],
                                  data["temperature"],
                                  data["humidity"],
                                  data["pressure"],
                                  data["windDirection"],
                                  data["windSpeed"],
                                  data["rain1h"],
                                  data["rain24h"],
                                  data["rain12h"],
                                  data["rain6h"],
                                  city["code"]
                                  ))
                conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    try:
        # create_tables()
        # save_areas()
        get_weather()
    except Exception as err:
        print(err)
