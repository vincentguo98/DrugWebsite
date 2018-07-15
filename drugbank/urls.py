from django.conf.urls import url
from . import views

app_name = "drugbank"

urlpatterns = [
	url('^ProjectionResult/',views.ProjectionResult,name="ProjectionResult"),
	url('^index/',views.index,name="index"),
	url('^search',views.search,name="search")
]