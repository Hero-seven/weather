# Generated by Django 2.0 on 2019-03-18 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='区域代码')),
                ('name', models.CharField(max_length=20, verbose_name='区域名称')),
                ('url', models.CharField(max_length=100, verbose_name='链接地址')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='weather_hour.City', verbose_name='上级区域')),
            ],
            options={
                'verbose_name': '区域',
                'verbose_name_plural': '区域',
                'db_table': 'tb_citys',
            },
        ),
        migrations.CreateModel(
            name='WeatherHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('date', models.DateField(unique=True, verbose_name='日期')),
                ('time', models.DateTimeField(unique=True, verbose_name='时间')),
                ('temperature', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='气温')),
                ('humidity', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='相对湿度')),
                ('pressure', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='气压')),
                ('windDirection', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='风向')),
                ('windSpeed', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='风速')),
                ('rain1h', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='1小时内降雨量')),
                ('rain24h', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='24小时内降雨量')),
                ('rain12h', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='12小时内降雨量')),
                ('rain6h', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='6小时内降雨量')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='weather_hour', to='weather_hour.City')),
            ],
            options={
                'verbose_name': '逐小时天气',
                'verbose_name_plural': '逐小时天气',
                'db_table': 'tb_weather_hour',
            },
        ),
    ]