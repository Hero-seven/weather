from django.db import models


# Create your models here.
class City(models.Model):
    """
    区域模型类
    """
    code = models.CharField("区域代码", primary_key=True, max_length=20, unique=True)
    name = models.CharField("区域名称", max_length=20)
    url = models.CharField("链接地址", max_length=100)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="subs", null=True, verbose_name="上级区域")

    class Meta:
        db_table = 'tb_citys'
        verbose_name = '区域'
        verbose_name_plural = '区域'

    def __str__(self):
        return self.name


class WeatherHour(models.Model):
    """逐小时天气数据
    """
    create_at = models.DateTimeField("创建时间", auto_now=True)
    date = models.DateField("日期")
    time = models.DateTimeField("时间", unique=True)
    temperature = models.FloatField("气温(℃)")
    humidity = models.FloatField("相对湿度(%)")
    pressure = models.FloatField("气压(hPa)")
    windDirection = models.FloatField("风向")
    windSpeed = models.FloatField("风速(m/s)")
    rain1h = models.FloatField("1小时内降雨量(mm)")
    rain24h = models.FloatField("24小时内降雨量(mm)")
    rain12h = models.FloatField("12小时内降雨量(mm)")
    rain6h = models.FloatField("6小时内降雨量(mm)")
    city = models.ForeignKey("City", on_delete=models.PROTECT, related_name="weather_hour")

    class Meta:
        db_table = 'tb_weather_hour'
        verbose_name = '逐小时天气'
        verbose_name_plural = '逐小时天气'
