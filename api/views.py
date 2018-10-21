from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.viewsets import ViewSet
from .serializers import *
from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from PIL import Image
from . import functions
import face_recognition
from django.core.files import File

Person = apps.get_model('server', 'Person')

Finger = apps.get_model('server', 'Finger')

Face = apps.get_model('server', 'Face')

Device = apps.get_model('server', 'Device')

PersonArrival = apps.get_model('server', 'PersonArrival')

PersonUnauthorizedEntry = apps.get_model('server', 'PersonUnauthorizedEntry')

class ImageUploadParser(FileUploadParser):
	media_type = 'image/*'

class VerifyViewSet(ViewSet):

	def verify(self, request, format = None):
		if(request.method=='POST'):
			if ('card_num' not in request.data):
				return Response({"message": "Error, empty content: card_num!"})
			try:
				person = Person.objects.get(card_num = (request.data['card_num']))
				return Response({"message": "True"})
			except:
				return Response({"message": "False"})

class MyViewSet(ViewSet):
	parser_class = (ImageUploadParser,)
	
	def verify(self, request, format = None):
		if(request.method=='POST'):
			if ('file' not in request.data):
				return Response({"message": "Error, empty content: file!"})
			if ( not ('card_num' in request.data or 'person_num' in request.data )):
				return Response({"message": "Error, empty content: card_num or person_num!"})
			
			if ('come_in' not in request.data):
				return Response({"message": "Error, empty content: come_in!"})

			if ('device_id' not in request.data):
				return Response({"message": "Error, empty content: device_id!"})

			f = request.data['file']
			come_in = request.data['come_in']
			
			device = ''
			try:
				device = Device.objects.get(pk=int(request.data['device_id']))
			except:
				return Response({"message": "No such device!"})

			person =  ''

			if 'card_num' in request.data :
				try:
					person = Person.objects.get(card_num=(request.data['card_num']))
				except:
					return Response({"message": "No such person!"})
			else :
				try:
					person = Person.objects.get(person_num=(request.data['person_num']))
				except:
					return Response({"message": "No such person!"})
			img =''
			try:
				img = Image.open(f)
				img.verify()
			except:
				return Response({"message": "Usupported image type!"})
			
			if img is  None:
				return Response({"message": "Usupported image type!"})

			img = face_recognition.load_image_file(f)
    
			face = ''
			try:
				face = Face.objects.filter(person = person)[0]
			except:
				return Response({"message": "No such image!"})

			dict = functions.find(img , face.image.path)
			responseMSG = {"message" : str(dict['flag'])}
			if dict['flag'] == True :
				newPA = PersonArrival()
				newPA.person = person
				newPA.device = device
				newPA.come_in = come_in
				newPA.image = f
				newPA.save()
				responseMSG.update({"saved" : "True"})
			else :
				newPUE = PersonUnauthorizedEntry();
				newPUE.person = person
				newPUE.device = device
				newPUE.image = f
				newPUE.save()
				responseMSG.update({"saved" : "False"})

			responseMSG.update({"distance" : dict['distance']})
			return Response(responseMSG)
		else :
			return Response({"message" : "Usupported method type"})

class PersonList(generics.ListCreateAPIView):
    
    queryset = Person.objects.all()
    model = Person
    serializer_class = PersonSerializer

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Person.objects.all()
    model = Person
    serializer_class = PersonSerializer

class FingerList(generics.ListCreateAPIView):
    
    queryset = Finger.objects.all()
    model = Finger
    serializer_class = FingerSerializer

class FingerDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Finger.objects.all()
    model = Finger
    serializer_class = FingerSerializer

class FaceList(generics.ListCreateAPIView):
    
    queryset = Face.objects.all()
    model = Face
    serializer_class = FaceSerializer

class FaceDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Face.objects.all()
    model = Face
    serializer_class = FaceSerializer
    
class DeviceList(generics.ListCreateAPIView):
    
    queryset = Device.objects.all()
    model = Device
    serializer_class = DeviceSerializer

class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Device.objects.all()
    model = Device
    serializer_class = DeviceSerializer
    
class PersonArrivalList(generics.ListCreateAPIView):
    
    queryset = PersonArrival.objects.all()
    model = PersonArrival
    serializer_class = PersonArrivalSerializer

class PersonArrivalDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = PersonArrival.objects.all()
    model = PersonArrival
    serializer_class = PersonArrivalSerializer

class PersonUnauthorizedEntryList(generics.ListCreateAPIView):
    
    queryset = PersonUnauthorizedEntry.objects.all()
    model = PersonUnauthorizedEntry
    serializer_class = PersonUnauthorizedEntrySerializer

class PersonUnauthorizedEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = PersonUnauthorizedEntry.objects.all()
    model = PersonUnauthorizedEntry
    serializer_class = PersonUnauthorizedEntrySerializer
