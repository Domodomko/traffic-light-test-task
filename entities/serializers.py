from rest_framework import serializers
from entities.models import (
    Client, 
    Contact, 
    Department, 
    ClientToDepartment, 
    Entity
)


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = (
            "id",
            "get_type_display",
            "value",
        )


class ClientToDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientToDepartment
        fields = (
            "id",
            "client",
            "client_identification_number",
            "client_full_name",
            "added_at",
        )


class DepartmentToClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientToDepartment
        fields = (
            "id",
            "department",
            "department_identification_number",
            "department_name",
            "added_at",
        )


class ClientSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)
    departments = DepartmentToClientSerializer(many=True)

    class Meta:
        model = Client
        fields = (
            "id",
            "identification_number",
            "phone_number",
            "first_name",
            "last_name",
            "patronymic",
            "updated_at",
            "get_type_display",
            "get_gender_display",
            "timezone",
            "is_active_updated_at",
            "contacts",
            "departments",
        )


class DepartmentSerializer(serializers.ModelSerializer):
    clients = ClientToDepartmentSerializer(many=True)

    class Meta:
        model = Department
        fields = (
            "id",
            "identification_number",
            "name",
            "parent",
            "parent_name",
            "entity",
            "entity_name",
            "clients",
        )


class EntitySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True)

    class Meta:
        model = Entity
        fields = (
            "id",
            "identification_number",
            "created_at",
            "updated_at",
            "full_name",
            "abbreviated_name",
            "inn",
            "ppc",
            "departments",
        )
