from rest_framework.response import Response
from rest_framework.views import APIView

from utils.get_weather_hour import save_areas, get_weather


class CityView(APIView):
    """保存城市信息
    """

    def get(self, request):
        # save_areas()
        return Response(data={"message": "OK"})


class WeatherView(APIView):

    def get(self, request):
        get_weather()
        return Response(data={"message": "OK"})
