from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from entities.managers import CustomUserManager
from entities.constants import TIMEZONES, ContactConstants, GenderConstants, ClientTypeConstants
from entities.mixins import AutoIdentificationNumberMixin


class Client(AutoIdentificationNumberMixin, AbstractUser):
    username = None

    identification_number = models.CharField(max_length=17, verbose_name="Идентификационный номер")
    phone_number = models.CharField(max_length=32, unique=True, verbose_name="Основной номер телефона")
    patronymic = models.CharField(max_length=32, null=True, blank=True, verbose_name="Отчество")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    type = models.PositiveSmallIntegerField(choices=ClientTypeConstants.CHOICES, default=ClientTypeConstants.PRIMARY,
                                            verbose_name="Тип")
    gender = models.PositiveSmallIntegerField(choices=GenderConstants.CHOICES, default=GenderConstants.UNKNOWN,
                                              verbose_name="Гендер")
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default="UTC", verbose_name="Часовой пояс")
    is_active_updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата изменения статуса")

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    __old_is_active = None
    identification_number_ending = "01"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.identification_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_is_active = self.is_active

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.is_active != self.__old_is_active:
            self.is_active_updated_at = timezone.now()

        super().save(force_insert, force_update, *args, **kwargs)
        self.__old_is_active = self.is_active


class Contact(models.Model):
    type = models.IntegerField(choices=ContactConstants.CHOICES, default=ContactConstants.EMAIL, verbose_name="Тип")
    value = models.CharField(max_length=32, verbose_name="Значение")
    client = models.ForeignKey("entities.Client", on_delete=models.CASCADE, verbose_name="Клиент")

    class Meta:
        verbose_name = "Контакт Клиента"
        verbose_name_plural = "Контакты Клиента"

    def clean(self):
        if Contact.objects.filter(type__in=ContactConstants.UNIQUE_CONTACT_TYPES_TUPLE, user=self.client,
                                  type=self.type).exists():
            raise ValidationError(
                {"type": f"У пользователя может быть только один контакт типа {self.get_type_display()}"})


class Entity(AutoIdentificationNumberMixin, models.Model):
    identification_number = models.CharField(max_length=17, blank=True, verbose_name="Идентификационный номер")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    full_name = models.CharField(max_length=32, verbose_name="Название полное")
    abbreviated_name = models.CharField(max_length=32, verbose_name="Название сокращенное")
    inn = models.CharField(max_length=32, verbose_name="ИНН")
    ppc = models.CharField(max_length=32, verbose_name="КПП")

    identification_number_ending = "02"

    class Meta:
        verbose_name = "Юридическое лицо"
        verbose_name_plural = "Юридические лица"

    def __str__(self):
        return self.identification_number


class Department(AutoIdentificationNumberMixin, MPTTModel):
    identification_number = models.CharField(max_length=17, blank=True, verbose_name="Идентификационный номер")
    name = models.CharField(max_length=32, verbose_name="Название")
    parent = TreeForeignKey(
        "self",
        verbose_name="Родительский департамент",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    entity = models.ForeignKey("entities.Entity", on_delete=models.CASCADE)

    __MAXIMUM_TREE_DEPTH = 7
    identification_number_ending = "03"

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"

    def __str__(self):
        return self.identification_number

    def clean(self):
        if self.parent:
            if self.parent.level == self.__MAXIMUM_TREE_DEPTH:
                raise ValidationError(
                    {"parent": f"Вы превысили максимальную вложенность ({self.__MAXIMUM_TREE_DEPTH})."})

    def clients_amount(self):
        return ClientToDepartment.objects.filter(department=self).count()

    clients_amount.short_description = "Количество клиентов"


class ClientToDepartment(models.Model):
    client = models.ForeignKey("entities.Client", on_delete=models.CASCADE, related_name="departments",
                               verbose_name="Клиент")
    department = models.ForeignKey("entities.Department", on_delete=models.CASCADE, related_name="clients",
                                   verbose_name="Департамент")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления в департамент")

    class Meta:
        verbose_name = "Клиент Департамента"
        verbose_name_plural = "Клиенты Департамента"
