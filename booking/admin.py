from django.contrib import admin
from .models import University,Dormitory,Profile,Resource,Booking


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name','city')

@admin.register(Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    list_display = ('name','university','address')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dormitory', 'role')
    list_filter = ('dormitory', 'role')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'dormitory', 'kind', 'is_active')
    list_filter = ('dormitory', 'kind', 'is_active')
    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'start', 'end')
    list_filter = ('resource__dormitory','resource')
    date_hierarchy = 'start'

