from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from entities.models import Contact, Client, Department


class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "identification_number", "updated_at", "is_active_updated_at"]


class ContactAdmin(admin.ModelAdmin):
    list_display = ["type", "client",]


class DepartmentAdmin(MPTTModelAdmin):
    list_display = ["name"]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Department, DepartmentAdmin)