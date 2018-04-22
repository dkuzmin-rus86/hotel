from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from slugify import slugify
import datetime

# Create your models here.


def default_code():
    Dt = datetime.datetime.now()
    return u'h%04d%02d%02d%02d%02d%02d' % (Dt.year, Dt.month, Dt.day, Dt.hour, Dt.minute, Dt.second)


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Region, self).__init__(*args, **kwargs)
        if self.name:
            self.slug = slugify(self.name)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class Filial(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Filial, self).__init__(*args, **kwargs)
        if self.name:
            self.slug = slugify(self.name)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        if self.name:
            self.slug = slugify(self.name)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Hotel(models.Model):
    name = models.CharField(max_length=512, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    filial = models.ForeignKey(Filial, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=512, blank=True)
    manager = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=128, blank=True)
    description = models.TextField(max_length=1024, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    deleted = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __init__(self, *args, **kwargs):
        super(Hotel, self).__init__(*args, **kwargs)
        if self.name:
            self.slug = slugify(self.name)

    def __str__(self):
        return self.name

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if self.name:
    #         self.slug = slugify(self.name)
    #         super(Hotel, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    # def save(self,  *args, **kwargs):
    #     if self.name:
    #         self.slug = slugify(self.name)
    #         return super(Hotel, self).save(*args, **kwargs)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    class Meta:
        permissions = (('cm_read_hotel_history', 'Просмотр истории изменений справочника Объекты размещения'),)
        verbose_name = 'Объект размещения'
        verbose_name_plural = 'Объекты размещения'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    filial = models.ForeignKey(Filial, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователя'


# class Guest(models.Model):
#     GENDER_CHOICES = (
#         ('male', 'Мужской'),
#         ('female', 'Женский')
#     )
#     CATEGORY_CHOICES = (
#         ('corporate', 'Корпоративный'),
#         ('outsider', 'Сторонняя организация')
#     )

#     guest_name = models.CharField(max_length=512)
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
#     year_of_birth = models.CharField(max_length=4, blank=True)
#     position = models.CharField(max_length=128, blank=True)

#     category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, blank=True)
#     document = models.CharField(max_length=1024, blank=True)
#     company = models.CharField(max_length=512, blank=True)
#     phone = models.CharField(max_length=128, blank=True)
#     city = models.CharField(max_length=128, blank=True)
#     created = models.DateTimeField(auto_now_add=True, auto_now=False)
#     updated = models.DateTimeField(auto_now_add=False, auto_now=True)
#     deleted = models.BooleanField(default=False)

#     history = HistoricalRecords()

#     def __str__(self):
#         return self.guest_name

#     def get_id(self):
#         return self.id

#     class Meta:
#         permissions = (('cm_read_guest_history', 'Просмотр истории изменений справочника гостей'),)
#         verbose_name = 'Гость'
#         verbose_name_plural = 'Гости'


class CategoryRoom(models.Model):
    name = models.CharField(max_length=512, blank=True)
    tarif = models.PositiveIntegerField(blank=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id

    class Meta:
        verbose_name = 'Категория номера'
        verbose_name_plural = 'Категории номеров'

# def delta(self):
#         if self.date2 >= self.date1 :
#             dt = abs(self.date2 - self.date1)
#             dt_days = dt.days + 1
#             hc = Holiday.objects.filter(holidays__range=[self.date1, self.date2]).count()
#             result = dt_days - hc
#             return str(result)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.DO_NOTHING, null=True)
    room_number = models.CharField(max_length=8)
    category_room = models.ForeignKey(CategoryRoom, on_delete=models.DO_NOTHING, null=True)
    primary_place = models.PositiveSmallIntegerField()
    secondary_place = models.PositiveSmallIntegerField()
    # status = models.CharField(max_length=128, blank=True)
    description = models.TextField(max_length=1024, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    deleted = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        return 'Комната: {}'.format(self.room_number)

    def get_id(self):
        return self.id

    def get_count_booking(self, date):
        result = Booking.objects.filter(deleted=False, room=self, chekin__lte=date, chekout__gte=date).count()
        return result

    class Meta:
        permissions = (('cm_read_room_history', 'Просмотр истории изменений справочника номеров'),)
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'


# placement
class Booking(models.Model):
    STATUS_CHOICES = (
        ('active', 'Проживает'),
        ('reserve', 'Бронь'),
        ('resident', 'Постоянно проживающий'),
        ('timeresident', 'Вахтовый работник'),
        ('cancel', 'Отмена')
    )
    PAYMENT_CHOICES = (
        ('withoutpay', 'Без оплаты'),
        ('cash', 'Наличная'),
        ('nocash', 'Безналичная')
    )
    GENDER_CHOICES = (
        ('male', 'Мужской'),
        ('female', 'Женский')
    )
    TYPE_PLACEMENT_CHOICES = (
        ('room', 'Номер'),
        ('prim_room', 'Место (основное)'),
        ('second_room', 'Место (дополнительное)')
    )

    code = models.CharField(max_length=15, blank=True)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, null=False)
    guest_name = models.CharField(max_length=512, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    birth_year = models.CharField(max_length=4, blank=True)
    position = models.CharField(max_length=128, blank=True)
    chekin = models.DateField(blank=True, null=True)
    chekout = models.DateField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True)
    type_placement = models.CharField(max_length=10, choices=TYPE_PLACEMENT_CHOICES, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True)
    payment = models.CharField(max_length=50, choices=PAYMENT_CHOICES, blank=True)
    description = models.TextField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    deleted = models.BooleanField(default=False)
    # guest = models.ForeignKey(Guest, on_delete=models.DO_NOTHING, null=True)
    # count_place_room = models.PositiveSmallIntegerField()
    # target = models.CharField(max_length=50, choices=TARGET_CHOICES, blank=True)

    history = HistoricalRecords()

    def __init__(self, *args, **kwargs):
        super(Booking, self).__init__(*args, **kwargs)
        self.code = default_code()

    # def save(self, *args, **kwargs):
    #     self.code = default_code()
    #     super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return 'Код размещения: {}'.format(self.id)

    def get_id(self):
        return self.id

    # def get_bookings_room(self, room, date):
    #     result = self.objects.filter(deleted=False, room=room, chekin___lte=date, chekout__gte=date).count()
    #     return result

    class Meta:
        permissions = (('cm_read_booking_history', 'Просмотр истории изменений таблицы размещения гостей в номерах'),)
        verbose_name = 'Размещение'
        verbose_name_plural = 'Размещения'
