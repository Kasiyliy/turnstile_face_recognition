from django.contrib import admin

from .models import Person,Face,PersonArrival,Device,Finger, PersonUnauthorizedEntry


class FaceAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        return super(FaceAdmin, self).save_model(request, obj, form, change)

class PersonUnauthorizedEntryAdmin(admin.ModelAdmin):
    
    fields = ['person' , 'image' , 'device', 'created' , 'image_tag' ,'image_tag2']
    readonly_fields = [ 'person' , 'image' , 'device', 'created' , 'image_tag', 'image_tag2']

	

class PersonArrivalAdmin(admin.ModelAdmin):
    
    readonly_fields = [ 'person' , 'image' , 'device', 'created' , 'come_in' , 'image_tag' ,'image_tag2']

    readonly_fields = [ 'person' , 'image' , 'device', 'created' , 'come_in' , 'image_tag' ,'image_tag2']

admin.site.register(Person)
admin.site.register(Face,FaceAdmin)
admin.site.register(PersonArrival,PersonArrivalAdmin)
admin.site.register(Device)
admin.site.register(Finger)
admin.site.register(PersonUnauthorizedEntry, PersonUnauthorizedEntryAdmin)
admin.site.site_header = 'Админ панель'
admin.site.index_title = 'Таблицы'
