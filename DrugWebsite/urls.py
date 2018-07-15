"""DrugWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import include
from django.conf.urls import url

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^Drug/',include('drugbank.urls'))
=======
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flight/', include('drug.urls')),
>>>>>>> 3c46ea715ad4cf04a5f78419f4f4144bdc77e7e2
]
