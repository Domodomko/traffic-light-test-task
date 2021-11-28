from django.db import transaction
from django.core.management.base import BaseCommand

import random
from factory.faker import faker
from tqdm import tqdm

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
        clients = ClientFactory.create_batch(CLIENTS_NUM)
        self.stdout.write(f"{CLIENTS_NUM} entities.contact objects are created!\n\n")

        self.stdout.write("Creating new entities.contact objects...")
        for client in tqdm(clients):
            Contact.objects.create(client=client, type=ContactConstants.EMAIL, value=FAKER.email())
            Contact.objects.create(client=client, type=ContactConstants.PHONE, value=FAKER.phone_number())
            Contact.objects.create(client=client, type=ContactConstants.VK, value=FAKER.user_name())
        self.stdout.write(f"entities.contact for entities.client objects are created!\n\n")

        self.stdout.write("Creating new entities.entity objects...")
        entities = EntityFactory.create_batch(ENTITIES_NUM)
        self.stdout.write(f"{ENTITIES_NUM} entities.entity objects are created!\n\n")

        # Did not use batch here to put random existing legal entities. Need to figure out how to put them with the batch.
        self.stdout.write("Creating new entities.department objects...")
        for _ in tqdm(range(DEPARTMENTS_NUM)):
            department_entity = random.choice(entities)
            department_clients = random.choices(clients, k=CLIENTS_PER_DEPARTMENT)
            department = DepartmentFactory(parent__parent__parent__parent__parent__parent__parent=None,
                                           entity=department_entity)
            for department_client in department_clients:
                for member in department.get_family():
                    ClientToDepartment.objects.create(department=member, client=department_client)
        self.stdout.write(f"{DEPARTMENTS_NUM} entities.department objects are created!")