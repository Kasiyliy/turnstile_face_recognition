from django.contrib import admin
from django.http import request

from .models import Person, PersonType,Face
from .models import PersonArrival,Device,Finger
from .models import PersonUnauthorizedEntry,Organization, ModeratorOrganization


class PersonTypeAdmin(admin.ModelAdmin):
    list_per_page = 10

class ModeratorOrganizationAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('get_moderator','organization',)

    def get_moderator(self, obj):
        return obj.moderator.username

    get_moderator.short_description = ModeratorOrganization._meta.get_field('moderator').verbose_name

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":
            if not request.user.is_superuser:
                try:
                    mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
                    kwargs["queryset"] = Person.objects.filter(organization=mod_organization.organization).all()
                except ModeratorOrganization.DoesNotExist:
                    kwargs["queryset"] = Person.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(FingerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        try:
            mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
            return qs.filter(person__organization=mod_organization.organization)
        except ModeratorOrganization.DoesNotExist:
            return Finger.objects.none()



class DeviceAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = ('organization', )
    list_display = ('name', 'organization')
    search_fields = ('name', 'organization__name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization":

            if not request.user.is_superuser:
                try:
                    mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
                    kwargs["queryset"] = Organization.objects.filter(pk=mod_organization.organization.pk).all()
                except ModeratorOrganization.DoesNotExist:
                    kwargs["queryset"] = Organization.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(DeviceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        try:
            mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
            return qs.filter(organization=mod_organization.organization)
        except ModeratorOrganization.DoesNotExist:
            return Device.objects.none()

class PersonAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('first_name', 'last_name' ,'middle_name' , 'organization__name' , 'person_type__name', 'iin')
    list_display = ('first_name', 'last_name' ,'middle_name' , 'organization' , 'person_type', 'iin')
    list_filter = ('organization', 'person_type')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization":

            if not request.user.is_superuser:
                try:
                    mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
                    kwargs["queryset"] = Organization.objects.filter(pk=mod_organization.organization.pk).all()
                except ModeratorOrganization.DoesNotExist:
                    kwargs["queryset"] = Organization.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        try:
            mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
            return qs.filter(organization=mod_organization.organization)
        except ModeratorOrganization.DoesNotExist:
            return Person.objects.none()


class FaceAdmin(admin.ModelAdmin):

    list_per_page = 10
    list_display = ('person' , 'image','get_person_iin')
    list_filter = ('person__organization',)
    search_fields = ('person__first_name', 'person__last_name', 'person__middle_name','image' )

    def get_person_iin(self, obj):
        return obj.person.iin

    get_person_iin.short_description = Person._meta.get_field('iin').verbose_name
    get_person_iin.admin_order_field = 'person__iin'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":

            if not request.user.is_superuser:
                try:
                    mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
                    kwargs["queryset"] = Person.objects.filter(organization=mod_organization.organization).all()
                except ModeratorOrganization.DoesNotExist:
                    kwargs["queryset"] = Person.objects.none()


        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        return super(FaceAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(FaceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        try:
            mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
            return qs.filter(person__organization=mod_organization.organization)
        except ModeratorOrganization.DoesNotExist:
            return Face.objects.none()

class PersonUnauthorizedEntryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('person' , 'device' , 'created')
    list_filter = ('person__organization','created','person__person_type')
    search_fields = ('person__first_name', 'person__last_name', 'person__middle_name', 'device__name' ,)
    fields = ['person' , 'image' , 'device',  'image_tag' ,'image_tag2']
    readonly_fields = ['image_tag', 'image_tag2']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":

            if not request.user.is_superuser:
                try:
                    mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
                    kwargs["queryset"] = Person.objects.filter(organization=mod_organization.organization ).all()
                except ModeratorOrganization.DoesNotExist:
                    kwargs["queryset"] = Person.objects.none()
        elif db_field.name == 'device':
            if not request.user.is_superuser:
                try:
                    mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
                    kwargs["queryset"] = Device.objects.filter(organization=mod_organization.organization).all()
                except ModeratorOrganization.DoesNotExist:
                    kwargs["queryset"] = Device.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(PersonUnauthorizedEntryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
            return qs.filter(person__organization=mod_organization.organization, device__organization=mod_organization.organization)
        except ModeratorOrganization.DoesNotExist:
            return PersonUnauthorizedEntry.objects.none()
	

class PersonArrivalAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('person', 'device', 'created')
    search_fields = ('person__first_name', 'person__last_name', 'person__middle_name', 'device__name',)
    list_filter = ('person__organization','created','person__person_type')
    fields = [ 'person' , 'image' , 'device', 'come_in' , 'image_tag' ,'image_tag2']

    readonly_fields = [ 'image_tag' ,'image_tag2']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":

            if not request.user.is_superuser:
                try:
                    mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
                    kwargs["queryset"] = Person.objects.filter(organization=mod_organization.organization).all()
                except ModeratorOrganization.DoesNotExist:
                    kwargs["queryset"] = Person.objects.none()
        elif db_field.name == 'device':
            if not request.user.is_superuser:
                try:
                    mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
                    kwargs["queryset"] = Device.objects.filter(organization=mod_organization.organization).all()
                except ModeratorOrganization.DoesNotExist:
                    kwargs["queryset"] = Device.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(PersonArrivalAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            mod_organization = ModeratorOrganization.objects.get(moderator=request.user)
            return qs.filter(person__organization=mod_organization.organization, device__organization=mod_organization.organization)
        except ModeratorOrganization.DoesNotExist:
            return PersonArrival.objects.none()



admin.site.register(ModeratorOrganization, ModeratorOrganizationAdmin)
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