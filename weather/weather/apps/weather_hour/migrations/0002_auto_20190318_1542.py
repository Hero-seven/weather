# Generated by Django 2.0 on 2019-03-18 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_hour', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherhour',
            name='humidity',
            field=models.FloatField(verbose_name='相对湿度'),
        ),
        migrations.AlterField(
            model_name='weatherhour',
            name='pressure',
            field=models.FloatField(verbose_name='气压'),
        ),
        migrations.AlterField(
            model_name='weatherhour',
            name='rain12h',
            field=models.FloatField(verbose_name='12小时内降雨量'),
        ),
        migrations.AlterField(
            model_name='weatherhour',
            name='rain1h',
            field=models.FloatField(verbose_name='1小时内降雨量'),
        ),
        migrations.AlterField(
            model_name='weatherhour',
            name='rain24h',
            field=models.FloatField(verbose_name='24小时内降雨量'),
        ),
        migrations.AlterField(
            model_name='weatherhour',
            name='rain6h',
            field=models.FloatField(verbose_name='6小时内降雨量'),
        ),
        migrations.AlterField(
            model_name='weatherhour',
            name='temperature',
            field=models.FloatField(verbose_name='气温'),
        ),
        migrations.AlterField(
            model_name='weatherhour',
            name='windDirection',
            field=models.FloatField(verbose_name='风向'),
        ),
        migrations.AlterField(
            model_name='weatherhour',
            name='windSpeed',
            field=models.FloatField(verbose_name='风速'),
        ),
    ]
