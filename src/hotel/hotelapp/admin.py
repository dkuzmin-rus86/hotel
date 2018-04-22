from django.contrib import admin
# from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from hotelapp.models import Hotel, CategoryRoom, Room, Booking, Event, Filial, Region
from hotelapp.models import UserProfile

# Register your models here.


class RegionAdmin(admin.ModelAdmin):
    pass


class FilialAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass


class HotelAdmin(admin.ModelAdmin):
    pass


class CategoryRoomAdmin(admin.ModelAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    pass


class GuestAdmin(admin.ModelAdmin):
    pass


class RoomTypeAdmin(admin.ModelAdmin):
    pass


class RoomAdmin(admin.ModelAdmin):
    pass


class BookingAdmin(admin.ModelAdmin):
    pass


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_filial')
    list_select_related = ('userprofile', )

    def get_filial(self, instance):
        return instance.userprofile.filial.name

    get_filial.short_description = 'Филиал'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Region, RegionAdmin)
admin.site.register(Filial, FilialAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(CategoryRoom, CategoryRoomAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)

# admin.site.register(UserProfile, UserProfileAdmin)
