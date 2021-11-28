import random
import string
import factory
from factory.django import DjangoModelFactory

from entities.models import Client, Entity, Department

digits = string.digits


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    patronymic = factory.Faker("last_name")
    phone_number = factory.Faker("phone_number")
    password = factory.PostGenerationMethodCall('set_password', 'slozhniy_parol')


class EntityFactory(DjangoModelFactory):
    class Meta:
        model = Entity

    full_name = factory.Faker("company")
    abbreviated_name = factory.Faker("company_suffix")
    inn = ''.join(random.choice(digits) for i in range(12))
    ppc = ''.join(random.choice(digits) for i in range(9))


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = factory.Faker("first_name")
    parent = factory.SubFactory('entities.factories.DepartmentFactory')
    entity = factory.SubFactory(EntityFactory)
