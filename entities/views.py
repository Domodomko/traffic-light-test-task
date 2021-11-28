from django.shortcuts import render

from rest_framework import generics

from entities.serializers import ClientSerializer, DepartmentSerializer, EntitySerializer
from entities.models import Client, Department, Entity


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all() \
        .prefetch_related("contacts", "departments", "departments__department")
    serializer_class = ClientSerializer


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all() \
        .select_related("parent", "entity") \
        .prefetch_related("clients", "clients__client")
    serializer_class = DepartmentSerializer


class EntityListView(generics.ListAPIView):
    queryset = Entity.objects.all() \
        .prefetch_related("departments__clients__client", "departments__parent")
    serializer_class = EntitySerializer
