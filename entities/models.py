from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from entities.managers import CustomUserManager
from entities.constants import TIMEZONES, ContactConstants, GenderConstants, ClientTypeConstants
from entities.mixins import AutoIdentificationNumberMixin

from utils.validators import validate_char_ending


# TODO get back validators
class Client(AbstractUser, AutoIdentificationNumberMixin):
    username = None

    identification_number = models.CharField(max_length=17, unique=True, validators=[])
    phone_number = models.CharField(max_length=32, unique=True)
    patronymic = models.CharField(max_length=32, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.PositiveSmallIntegerField(choices=ClientTypeConstants.CHOICES, default=ClientTypeConstants.PRIMARY)
    gender = models.PositiveSmallIntegerField(choices=GenderConstants.CHOICES, default=GenderConstants.UNKNOWN)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default="UTC")
    is_active_updated_at = models.DateTimeField(auto_now_add=True,)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    __old_is_active = None
    identification_number_ending = "01"
    
    def __str__(self):
        return self.identification_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_is_active = self.is_active
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        last_client = Client.objects.latest('pk')
        self.identification_number = "{:012d}".format(last_client.pk+1) + "01"

        if self.is_active != self.__old_is_active:
            self.is_active_updated_at = timezone.now()
        
        super().save(force_insert, force_update, *args, **kwargs)
        self.__old_is_active = self.is_active


class Contact(models.Model):
    type = models.IntegerField(choices=ContactConstants.CHOICES ,default=ContactConstants.EMAIL,)
    value = models.CharField(max_length=32)
    client = models.ForeignKey(Client, on_delete=models.CASCADE,)
    
    def clean(self):
        if Contact.objects.filter(type__in=ContactConstants.UNIQUE_CONTACT_TYPES_TUPLE, user=self.client, type=self.type).exists():
            raise ValidationError({"type": f"У пользователя может быть только один контакт типа {self.get_type_display()}"})


class Entity(models.Model, AutoIdentificationNumberMixin):
    identification_number = models.CharField(max_length=17, unique=True, validators=[])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=32)
    abbreviated_name = models.CharField(max_length=32)
    inn = models.CharField(max_length=32)
    ppc = models.CharField(max_length=32)

    identification_number_ending = "02"

    def __str__(self):
        return self.identification_number


class Department(AutoIdentificationNumberMixin, MPTTModel):
    identification_number = models.CharField(max_length=17, blank=True)
    name = models.CharField(max_length=32)
    parent = TreeForeignKey(
        "self",
        verbose_name="Родительский департамент",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    __MAXIMUM_TREE_DEPTH = 7
    identification_number_ending = "03"

    def __str__(self):
        return self.identification_number
    
    def clean(self):
        if self.parent:
            if self.parent.level == self.__MAXIMUM_TREE_DEPTH:
                raise ValidationError({"parent": f"Вы превысили максимальную вложенность ({self.__MAXIMUM_TREE_DEPTH})."})
