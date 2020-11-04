from django.contrib import admin

from .models import Address


class AddressAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["zip_code", "address", "number", "complement"]


admin.site.register(Address, AddressAdmin)
