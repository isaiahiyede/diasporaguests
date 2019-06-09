from django.contrib import admin
from models import RoomType, RoomNumber


# Register your models here.

class RoomTypeAdmin(admin.ModelAdmin):
    search_fields = ['room_type']

admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(RoomNumber)


