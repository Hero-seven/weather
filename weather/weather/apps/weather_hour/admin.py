from django.contrib import admin

# Register your models here.
from weather_hour.models import City, WeatherHour


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "url", "parent")


@admin.register(WeatherHour)
class WeatherHourAdmin(admin.ModelAdmin):
    list_display = ("create_at", "date", "time", "city", "temperature",
                    "humidity", "pressure", "windDirection", "windSpeed",
                    "rain1h", "rain24h", "rain12h", "rain6h")
