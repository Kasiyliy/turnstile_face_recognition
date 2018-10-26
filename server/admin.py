from django.contrib import admin
from django.http import request

from .models import Person, PersonType,Face,PersonArrival,Device,Finger, PersonUnauthorizedEntry,Organization

class PersonTypeAdmin(admin.ModelAdmin):
    list_per_page = 10

class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_per_page = 10

class FingerAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('person__first_name', 'person__last_name','person__middle_name' ,'finger_num')
    list_display = ('person', 'finger_num', 'get_organization')

    def get_organization(self, obj):
        return obj.person.organization

    get_organization.short_description = Organization._meta.verbose_name.title()
    get_organization.admin_order_field = 'person__organization'


class DeviceAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = ('organization', )
    list_display = ('name', 'organization')
    search_fields = ('name', 'organization__name')

class PersonAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('first_name', 'last_name' ,'middle_name' , 'organization__name' , 'person_type__name')
    list_display = ('first_name', 'last_name' ,'middle_name' , 'organization' , 'person_type')
    list_filter = ('organization', 'person_type')


class FaceAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('person' , 'image')
    list_filter = ('person__organization',)
    search_fields = ('person__first_name', 'person__last_name', 'person__middle_name','image' )
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":
            kwargs["queryset"] = Person.objects.filter(face__isnull=True).all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        return super(FaceAdmin, self).save_model(request, obj, form, change)



class PersonUnauthorizedEntryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('person' , 'device' , 'created')
    list_filter = ('person__organization','created','person__person_type')
    search_fields = ('person__first_name', 'person__last_name', 'person__middle_name', 'device__name' ,)
    fields = ['person' , 'image' , 'device',  'image_tag' ,'image_tag2']
    readonly_fields = ['image_tag', 'image_tag2']

	

class PersonArrivalAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('person', 'device', 'created')
    search_fields = ('person__first_name', 'person__last_name', 'person__middle_name', 'device__name',)
    list_filter = ('person__organization','created','person__person_type')
    fields = [ 'person' , 'image' , 'device', 'come_in' , 'image_tag' ,'image_tag2']

    readonly_fields = [ 'image_tag' ,'image_tag2']

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonType, PersonTypeAdmin)
admin.site.register(Face, FaceAdmin)
admin.site.register(PersonArrival, PersonArrivalAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Finger, FingerAdmin)
admin.site.register(PersonUnauthorizedEntry, PersonUnauthorizedEntryAdmin)
admin.site.site_header = 'Админ панель'
admin.site.index_title = 'Таблицы'