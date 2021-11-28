import pytz


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class ContactConstants:
    EMAIL = 1
    PHONE = 2
    VK = 3
    FACEBOOK = 4
    OK = 5
    INSTAGRAM = 6
    TELEGRAM = 7
    WHATSAPP = 8
    VIBER = 9

    CHOICES = [
        (EMAIL, "Дополнительный email"),
        (PHONE, "Дополнительный телефон"),
        (VK, "ВКонтакте"),
        (FACEBOOK, "Facebook"),
        (OK, "Одноклассники"),
        (INSTAGRAM, "Instagram"),
        (TELEGRAM, "Telegram"),
        (WHATSAPP, "WhatsApp"),
        (VIBER, "Viber"),
    ]

    UNIQUE_CONTACT_TYPES_TUPLE = (
        OK,
        INSTAGRAM,
        TELEGRAM,
        WHATSAPP,
        VIBER,
    )


class GenderConstants:
    MALE = 1
    FEMALE = 2
    UNKNOWN = 3

    CHOICES = [
        (MALE, "Мужской"),
        (FEMALE, "Женский"),
        (UNKNOWN, "Неизвестно"),
    ]


class ClientTypeConstants:
    PRIMARY = 1
    REPEATED = 2
    EXTERNAL = 3
    INDIRECT = 4

    CHOICES = [
        (PRIMARY, "Первичный"),
        (REPEATED, "Повторный"),
        (EXTERNAL, "Внешний"),
        (INDIRECT, "Косвенный")
    ]