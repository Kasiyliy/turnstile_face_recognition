from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    #PERSON
    url(r'persons/(?P<pk>[0-9]+)$', PersonDetail.as_view(), name="person-detail"),
    url('persons', PersonList.as_view(), name="person-list"),
    
    #Finger
    url(r'fingers/(?P<pk>[0-9]+)$', FingerDetail.as_view(), name="finger-detail"),
    url('fingers', FingerList.as_view(), name="person-list"),
    
    #Face
    url(r'faces/(?P<pk>[0-9]+)$', FaceDetail.as_view(), name="face-detail"),
    url('faces', FaceList.as_view(), name="face-list"),

    #Device
    url(r'devices/(?P<pk>[0-9]+)$', DeviceDetail.as_view(), name="device-detail"),
    url('devices', DeviceList.as_view(), name="device-list"),

    #Organization
    url(r'organizations/(?P<pk>[0-9]+)$', DeviceDetail.as_view(), name="organization-detail"),
    url('organizations', DeviceList.as_view(), name="organization-list"),

    #PersonArrival
    url(r'person_arrival/(?P<pk>[0-9]+)$', PersonArrivalDetail.as_view(), name="person-arrival-detail"),
    url('person_arrival', PersonArrivalList.as_view(), name="person-arrival-list"),

    #PersonUnauthorizedEntry
    url(r'person_unauthorized_entry/(?P<pk>[0-9]+)$', PersonUnauthorizedEntryDetail.as_view(), name="person-unauthorized-entry-detail"),
    url('person_unauthorized_entry', PersonUnauthorizedEntryList.as_view(), name="person-unauthorized-entry-ist"),

    url(r'get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),

    url(r'verify/card/$', VerifyViewSet.as_view({'post' : 'verify'}), name='verify-card'),
    
    url(r'verify/$', MyViewSet.as_view({'post' : 'verify'}), name='verify'),

]

urlpatterns = format_suffix_patterns(urlpatterns)