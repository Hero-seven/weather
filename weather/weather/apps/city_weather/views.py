from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .serializers import AreaSerializer, AreaSubsSerializer
from .models import Area
from weather.settings import BASE_DIR
import csv
import os


# Create your views here.
class AreasView(ViewSet):
    """
    省市区三级联动
    """

    def list(self, request):
        """
        1.查询所有省
        2.序列化输出
        """
        provinces = Area.objects.filter(parent=None)
        serializer = AreaSerializer(provinces, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """
        1.根据pk,查询该省/市级下的所有市/县区
        2.序列化输出
        """
        try:
            area = Area.objects.get(pk=pk)
        except Exception as e:
            return Response({"message": "抱歉,暂时没有该地区数据！"})
        serializer = AreaSubsSerializer(area)
        return Response(serializer.data)


class DataView(APIView):
    """首页显示图表"""

    def get(self, request, district_id):
        # 获取城市名称
        city_name = Area.objects.get(id=int(district_id)).name
        # city_name = city_name[:-1] if len(city_name) > 2 else city_name
        # 查询该城市的降水量数据
        file_path = os.path.join(os.path.dirname(BASE_DIR), 'utils/data/precipitation.csv')
        precipitation_data = []
        with open(file_path) as f:
            data_list = csv.reader(f)
            for data in data_list:
                if data[2] == city_name:
                    precipitation_data = [float(i) for i in data[3:]]

        # 查询该城市的气温数据
        file_path = os.path.join(os.path.dirname(BASE_DIR), 'utils/data/temperature.csv')
        temperature_data = []
        with open(file_path) as f:
            data_list = csv.reader(f)
            for data in data_list:
                if data[2] == city_name:
                    temperature_data = [float(i) for i in data[3:]]
        print(temperature_data)
        # 构造数据
        data = {
            "precipitation_data": precipitation_data,
            "temperature_data": temperature_data,
            "district_name": city_name,
        }
        return Response(data)
