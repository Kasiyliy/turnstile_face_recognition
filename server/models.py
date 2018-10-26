from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User



class PersonType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип пользователя'
        verbose_name_plural = 'Типы пользователей'

class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование организации')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class ModeratorOrganization(models.Model):
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Модератор')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     verbose_name=Organization._meta.verbose_name.title())
    class Meta:
        verbose_name = 'Организация модератора'
        verbose_name_plural = 'Организации модераторов'



class Person(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200 , verbose_name='Фамилия')
    middle_name = models.CharField(max_length=200, default='' , verbose_name='Отчество')
    card_num = models.CharField(max_length=8, null=True, blank=True, verbose_name='Номер карты' , unique=True)
    person_num = models.CharField(max_length=100, null=True, blank=True, verbose_name='Номер человека', unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, verbose_name='Организация', null=True, blank=False)
    person_type = models.ForeignKey(PersonType, on_delete=models.SET_NULL, verbose_name='Тип пользователя', null=True ,blank=False)
    birth_date = models.DateTimeField( verbose_name='День рождения')
    created = models.DateTimeField(
            default=timezone.now,verbose_name='Дата создания')
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + self.middle_name
        
    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        
class Finger(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='ФИО')
    finger_num = models.BigIntegerField(unique=True, null=True, verbose_name='Код отпечатка пальца')
    
    def __str__(self):
        return self.person.first_name + ' ' + self.person.last_name + ' ' + self.person.middle_name + ': ' + str(self.finger_num)
        
    class Meta:
        verbose_name = 'Отпечаток пальца'
        verbose_name_plural = 'Отпечатки пальцев'

class Face(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name='ФИО', primary_key=True)
    image = models.ImageField(verbose_name='Фото', default= 'noimage.jpg', upload_to='faces')
    
    def __str__(self):
        return  self.person.first_name + ' '+ self.person.last_name + ' ' + self.person.middle_name + ': '+Face._meta.verbose_name.title()
        
    class Meta:
        verbose_name = 'Снимок лица'
        verbose_name_plural = 'Снимки лиц'

class Device(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название устройства')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация', null = True, blank=False)

    def __str__(self):
        result = 'ID: ' + str(self.id) + ', '
        if self.organization is not None:
            result += Organization._meta.get_field('name').verbose_name.lower() + ':  ' + self.organization.name + ', '
        result += self._meta.get_field('name').verbose_name.lower() + ': ' + self.name
        return result
        
    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'



class PersonArrival(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='ФИО')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
    come_in = models.BooleanField(verbose_name='Зашёл')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(verbose_name='Фото' , default= 'noimage.jpg' ,  upload_to='person_arrivals')


    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="/media/{}" width="150" height="150" />'.format(self.image))
    image_tag.short_description = ' Вошедший человек '    

    def image_tag2(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="/media/{}" width="150" height="150" />'.format((Face.objects.get(person=self.person)).image))
    image_tag2.short_description = ' Реальный человек ' 

    def __str__(self):
        person = Person.objects.get(pk=self.person_id)
        if (self.come_in == True):
            res = 'Вошел в: '
        else:
            res = 'Вышел в: '
        return person.last_name + ' ' + person.first_name + ' ' + person.middle_name + ' ' + res + ' ' + str(self.created)   
    
    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'


class PersonUnauthorizedEntry(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='ФИО')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Устройство')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(verbose_name='Фото', default= 'noimage.jpg', upload_to='person_unauthorized_arrivals')

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="/media/{}" width="150" height="150" />'.format(self.image))
    image_tag.short_description = ' Пытавшийся войти человек '    

    def image_tag2(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="/media/{}" width="150" height="150" />'.format((Face.objects.get(person=self.person)).image))
    image_tag2.short_description = ' Реальный человек '    

    
    
    

    def __str__(self):
        
        return self.person.last_name + ' ' + self.person.first_name + ' ' + self.person.middle_name + ' - ' + self.device.name + ' :' + str(self.created)
    
    class Meta:
        verbose_name = 'История несанкционированных входов'
        verbose_name_plural = 'Истории несанкционированных входов'


@receiver(pre_delete, sender=Face)
def face_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if(instance.image.name!='noimage.jpg'):
        instance.image.delete(False)

@receiver(pre_delete, sender=PersonArrival)
def person_arrival_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if(instance.image.name!='noimage.jpg'):
        instance.image.delete(False)

@receiver(pre_delete, sender=PersonUnauthorizedEntry)
def person_unauthorized_arrival_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if(instance.image.name!='noimage.jpg'):
        instance.image.delete(False)
    