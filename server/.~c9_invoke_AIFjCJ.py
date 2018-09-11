from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.index, name='index'),
    url('main-page', main_p.index, name='main_page'),
]