"""roll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from lunch import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.create_index),
    url(r'^create$', views.create, name='create'),
    url(r'^eatwhat/', views.index, name="eatwhat"),
    url(r'^roll$', views.roll, name='add'),
    url(r'^result/', views.result_view, name='result'),
    url(r'^bill$', views.bill, name='bill'),
    url(r'^bill/confirm$', views.bill_claim_confirm, name="bill_confirm"),
    url(r'^bill/submit', views.bill_claim_submit, name="bill_submit"),
    url(r'^settle', views.settle, name="settle"),
    url(r'^list$', views.lists, name="list")

]
