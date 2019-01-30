from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

urlpatterns = [
    url(r'^areas/$', views.AreasView.as_view({"get": "list"})),
    url(r'^areas/(?P<pk>\d+)/$', views.AreasView.as_view({"get": "retrieve"})),
    url(r'^index/(?P<district_id>\d+)/$', views.DataView.as_view()),

]

# router = SimpleRouter()
# router.register(r"areas", views.AreasView, base_name="area")
# urlpatterns += router.urls