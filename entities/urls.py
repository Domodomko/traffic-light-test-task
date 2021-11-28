from django.urls import include, path

from entities.views import ClientListView, DepartmentListView, EntityListView

urlpatterns = [
    path('api/clients', ClientListView.as_view(), name='clients'),
    path('api/departments', DepartmentListView.as_view(), name='departments'),
    path('api/entities', EntityListView.as_view(), name='entities'),
]
