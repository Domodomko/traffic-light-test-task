from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from entities.models import (
    Contact,
    Client,
    Contact,
    Department,
    Entity,
    ClientToDepartment
)


class ContactInline(admin.TabularInline):
    model = Contact
    fields = ["type", "value"]
    extra = 1


class ClientsInline(admin.TabularInline):
    model = ClientToDepartment
    fields = ["client", "added_at"]
    readonly_fields = ["added_at"]
    extra = 1


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "identification_number",
        "updated_at",
        "is_active_updated_at",
    ]

    fields = [
        "identification_number",
        "phone_number",
        "first_name",
        "last_name",
        "patronymic",
        "date_joined",
        "updated_at",
        "is_active_updated_at",
        "is_active",
        "type",
        "gender",
        "timezone",
    ]

    readonly_fields = [
        "identification_number",
        "date_joined",
        "updated_at",
        "is_active_updated_at",
    ]

    inlines = [ContactInline, ]


class DepartmentAdmin(MPTTModelAdmin):
    list_display = [
        "identification_number",
        "name",
        "clients_amount"
    ]
    fields = [
        "identification_number",
        "name",
        "parent",
        "entity"
    ]
    readonly_fields = ["identification_number", ]
    inlines = [ClientsInline, ]


class EntityAdmin(admin.ModelAdmin):
    list_display = [
        "identification_number",
        "full_name",
        "created_at",
    ]

    fields = [
        "identification_number",
        "created_at",
        "updated_at",
        "full_name",
        "abbreviated_name",
        "inn",
        "ppc",
    ]

    readonly_fields = [
        "identification_number",
        "created_at",
        "updated_at",
    ]

    inlines = [DepartmentInline, ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Entity, EntityAdmin)
