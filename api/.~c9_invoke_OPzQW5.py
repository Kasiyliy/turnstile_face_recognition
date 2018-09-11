from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PersonList, PersonDetail
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    url(r'persons/(?P<pk>[0-9]+)$', PersonDetail.as_view(), name="person-detail"),
    url('persons', PersonList.as_view(), name="person-list"),
    url(r'get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]

urlpatterns = format_suffix_patterns(urlpatterns)