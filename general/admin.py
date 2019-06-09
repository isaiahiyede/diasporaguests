from django.contrib import admin
from models import UserAccount, Bookings


# Register your models here.

class UserAccountAdmin(admin.ModelAdmin):
    search_fields = ['room_type']

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Bookings)

# Register your models here.
