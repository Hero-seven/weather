import time
import requests
import psycopg2

from lxml import etree
from pprint import pprint


def create_table_areas():
    """创建省市区地址表
    """
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()

    sql = """CREATE TABLE areas_sun(code varchar(20) primary key not null,
                                    name varchar(20),
                                    url varchar(100),
                                    parent varchar(20)
                                    );"""
    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()


def create_table_sun():
    """创建日出日落时间数据表
    """
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()

    # 创建天气数据表
    sql = """CREATE TABLE sun(code varchar,
                            city varchar,
                            city_detail varchar,
                            date_formatted varchar,
                            date date,
                            lat float,
                            lng float,
                            timezone varchar,
                            sunrise timestamp,
                            sunset timestamp,
                            sun_duration varchar
                            );"""
    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()


def get_provinces(conn, cur):
    """获取所有省份
    """
    url = "http://richuriluo.qhdi.com/poi/172496.html"
    response = requests.get(url)
    content = response.content.decode("utf-8")
    eroot = etree.HTML(content)

    province_url_list = eroot.xpath("//div[@class='clearfix']/a/@href")[:-2]
    name_list = eroot.xpath("//div[@class='clearfix']/a/text()")

    provinces = []
    for i, url in enumerate(province_url_list):
        code = url.split(".")[0][-6:]
        data = {
            "code": code,
            "name": name_list[i],
            "url": url,
        }
        # 保存数据至数据库
        sql = "INSERT INTO areas_sun values (%s,%s,%s)"
        cur.execute(sql, (data["code"], data["name"], data["url"]))
        conn.commit()

        provinces.append(data)
    return provinces


def get_cities(province, conn, cur):
    """获取所有市级
    """
    url = "http://richuriluo.qhdi.com" + province["url"]
    response = requests.get(url)
    content = response.content.decode("utf-8")
    eroot = etree.HTML(content)

    city_url_list = eroot.xpath("//div[@class='clearfix']/a/@href")[:-2]
    name_list = eroot.xpath("//div[@class='clearfix']/a/text()")

    cities = []
    for i, url in enumerate(city_url_list):
        code = url.split(".")[0][-6:]
        data = {
            "code": code,
            "name": name_list[i],
            "url": url,
            "parent": province["code"]
        }
        # 保存数据至数据库
        sql = "INSERT INTO areas_sun values (%s,%s,%s,%s)"
        cur.execute(sql, (data["code"], data["name"], data["url"], data["parent"]))
        conn.commit()

        cities.append(data)
    # pprint(cities)
    return cities


def get_districts(city, conn, cur):
    """获取县区级
    """
    url = "http://richuriluo.qhdi.com" + city["url"]
    try:
        response = requests.get(url)
        content = response.content.decode("utf-8")
        eroot = etree.HTML(content)
        district_url_list = eroot.xpath("//div[@class='clearfix']/a/@href")[:-2]
        name_list = eroot.xpath("//div[@class='clearfix']/a/text()")
    except Exception:
        return

    for i, url in enumerate(district_url_list):
        code = url.split(".")[0][-6:]
        data = {
            "code": code,
            "name": name_list[i],
            "url": url,
            "parent": city["code"]
        }
        print(data)
        # 保存数据至数据库
        sql = "INSERT INTO areas_sun values (%s,%s,%s,%s)"
        cur.execute(sql, (data["code"], data["name"], data["url"], data["parent"]))
        conn.commit()


def save_areas():
    """获取省市区信息并保存
    """
    # 连接数据库
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()
    # 省
    provinces = get_provinces(conn, cur)
    for province in provinces:
        # 市
        cities = get_cities(province, conn, cur)
        for city in cities:
            # 区
            get_districts(city, conn, cur)

    cur.close()
    conn.close()


def sun_gps(addr, conn, cur):
    """获取某城市的经纬度和全年日出日落时间
    """
    url = "http://richuriluo.qhdi.com" + addr["url"]
    response = requests.get(url)
    content = response.content.decode("utf-8")
    eroot = etree.HTML(content)
    if eroot is not None:
        # 获取地址、经纬度、时区
        address_detail = eroot.xpath("//div[@class='content-left']/h4[1]/text()")[0][3:]
        EN = eroot.xpath("//div[@class='content-left']/h4[2]/text()")[0]
        lat = EN.split(",")[0][6:]
        lng = EN.split(",")[1][2:]
        timezone = eroot.xpath("//div[@class='content-left']/h4[3]/text()")[0][3:]

        # 获取日出日落时间及日照时长
        base_str = "//div[@class='content-left']//table[@id='detail-table']"
        element_tr = eroot.xpath(base_str + "//tr")  # 获取表格数据条数
        count = len(element_tr)

        for i in range(count - 1):
            date_formatted = eroot.xpath(base_str + "//tr[{}]/td[1]/text()".format(i + 2))[0]
            sunrise = \
                eroot.xpath(base_str + "//tr[{}]/td[2]/span[@class='sun-time']/@data-timestamp".format(i + 2))[0]
            sunset = eroot.xpath(base_str + "//tr[{}]/td[3]/span[@class='sun-time']/@data-timestamp".format(i + 2))[
                0]
            sun_duration = eroot.xpath(base_str + "//tr[{}]/td[4]/text()".format(i + 2))[0]
            date = time.strftime("%Y-%m-%d", time.localtime(int(sunrise)))

            data = {"code": addr["code"],
                    "city": addr["name"],
                    "city_detail": address_detail,
                    "date_formatted": date_formatted,
                    "date": date,
                    "lat": lat,
                    "lng": lng,
                    "timezone": timezone,
                    "sunrise": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(sunrise))),
                    "sunset": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(sunset))),
                    "sun_duration": sun_duration,
                    }
            pprint(data)

            sql = "INSERT INTO sun values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(sql, (data["code"],
                              data["city"],
                              data["city_detail"],
                              data["date_formatted"],
                              data["date"],
                              data["lat"],
                              data["lng"],
                              data["timezone"],
                              data["sunrise"],
                              data["sunset"],
                              data["sun_duration"]
                              ))
            conn.commit()


def save_sun():
    """获取并保存数据：经纬度及和全年日出日落时间
    """
    # 连接数据库
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()

    # 获取地址信息
    cur.execute("SELECT * FROM areas_sun;")
    addrs = cur.fetchall()

    # 获取已保存数据的地址
    cur.execute("select distinct code from sun;")
    codes = cur.fetchall()
    code_list = [code[0] for code in codes]

    for addr in addrs:
        if addr[0] not in code_list:
            data = {
                "code": addr[0],
                "name": addr[1],
                "url": addr[2],
                "parent": addr[3]
            }
            # print(data)

            sun_gps(data, conn, cur)

    cur.close()
    conn.close()


def get_tables():
    # 连接数据库
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()

    # 获取地址信息
    cur.execute("select table_name from information_schema.tables where table_schema='public';")
    tables = cur.fetchall()
    table_list = [table[0] for table in tables]
    # print(table_list)

    cur.close()
    conn.close()
    return table_list


def main():

    tables = get_tables()

    if "areas_sun" not in tables:
        # 创建省市区地址表
        create_table_areas()
        # 获取并保存省市区信息
        save_areas()

    if "sun" not in tables:
        # 创建日出日落时间表
        create_table_sun()
    # 获取并保存日出日落时间及经纬度信息
    save_sun()


if __name__ == '__main__':
    main()
