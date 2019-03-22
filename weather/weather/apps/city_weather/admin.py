from django.contrib import admin

from city_weather.models import Area


@admin.register(Area)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "parent")
