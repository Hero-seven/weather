import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["simhei"]
plt.rcParams["axes.unicode_minus"] = False


def draw_chart(data, row, city):
    """绘制图表"""
    # 获取城市的降水量数据
    city_data = data.loc[city, row]

    # 绘制图表
    city_data.plot(kind='bar', figsize=(20, 8), colormap='Blues_r')

    # 自定义x,y轴刻度
    x_ticks = ['{}月'.format(i) for i in range(1, 13)]
    x = range(len(x_ticks))
    y_ticks = range(201)
    plt.xticks(x, x_ticks, rotation=0, size=18)
    plt.yticks(y_ticks[::50], size=18)

    # 添加x,y轴描述信息及标题
    plt.xlabel("月份", size=20)
    plt.ylabel("降水量(mm)", size=20)
    plt.title("{}每月降水量统计".format(city), size=24)

    # 保存图表
    plt.savefig("./graphes/{}.png".format(city), dpi=200)


def main():
    # 读取数据
    csv_data = pd.read_csv("./backup/precipitation.csv")
    # 设置索引
    data = csv_data.set_index("city")
    # 指定数据行
    row = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

    # 遍历每个城市数据,绘制图形
    citys = data.index
    for city in citys:
        draw_chart(data, row, city)


if __name__ == '__main__':
    main()
