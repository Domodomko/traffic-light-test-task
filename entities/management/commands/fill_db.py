from django.db import transaction
from django.core.management.base import BaseCommand

import random
from factory.faker import faker

from entities.models import Contact, ClientToDepartment
from entities.constants import ContactConstants
from entities.factories import ClientFactory, EntityFactory, DepartmentFactory

FAKER = faker.Faker()

CLIENTS_NUM = 30000
ENTITIES_NUM = 200
DEPARTMENTS_NUM = 100  # It creates 7 items at a time
CLIENTS_PER_DEPARTMENT = 5


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        clients = []
        entities = []

        self.stdout.write("Creating new entities.client objects...")
        for _ in range(CLIENTS_NUM):
            client = ClientFactory()
            Contact.objects.create(client=client, type=ContactConstants.EMAIL, value=FAKER.email())
            Contact.objects.create(client=client, type=ContactConstants.PHONE, value=FAKER.phone_number())
            Contact.objects.create(client=client, type=ContactConstants.VK, value=FAKER.user_name())
            clients.append(client)

        self.stdout.write("Creating new entities.entity objects...")
        for _ in range(ENTITIES_NUM):
            entity = EntityFactory()
            entities.append(entity)

        self.stdout.write("Creating new entities.department objects...")
        for _ in range(DEPARTMENTS_NUM):
            department_entity = random.choice(entities)
            department_clients = random.choices(clients, k=CLIENTS_PER_DEPARTMENT)
            department = DepartmentFactory(parent__parent__parent__parent__parent__parent__parent=None,
                                           entity=department_entity)
            for department_client in department_clients:
                for member in department.get_family():
                    ClientToDepartment.objects.create(department=member, client=department_client)
