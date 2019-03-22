from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^city/$', views.CityView.as_view()),
    url(r'^weather/hour/$', views.WeatherView.as_view()),
]