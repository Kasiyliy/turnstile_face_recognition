from rest_framework import serializers
from django.apps import apps
Person = apps.get_model('server', 'Person')

Finger = apps.get_model('server', 'Finger')

Face = apps.get_model('server', 'Face')

Device = apps.get_model('server', 'Device')

PersonArrival = apps.get_model('server', 'PersonArrival')

PersonUnauthorizedEntry = apps.get_model('server', 'PersonUnauthorizedEntry')

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Person
        fields = ('id', 'first_name', 'last_name', 'middle_name','card_num', 'birth_date' , 'created')
        read_only_fields = ('created',)

class FingerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Finger
        fields = ('id', 'person', 'finger_num')

class FaceSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(max_length=None,use_url=True)
    
    class Meta:

        model = Face
        fields = ('id', 'person', 'image')

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Device
        fields = ('id', 'name')

class PersonArrivalSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(max_length=None,use_url=True)
    
    class Meta:

        model = PersonArrival
        fields = ('id', 'person' , 'device', 'come_in','image' , 'created')
        read_only_fields = ('created',)

class PersonUnauthorizedEntrySerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(max_length=None,use_url=True)

    class Meta:

        model = PersonUnauthorizedEntry
        fields = ('id', 'person' , 'device', 'image' , 'created')
        read_only_fields = ('created',)