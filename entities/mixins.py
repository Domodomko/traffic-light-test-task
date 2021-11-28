from django.core.exceptions import ObjectDoesNotExist


class AutoIdentificationNumberMixin:
    identification_number_ending = "01"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print("AutoIdentificationNumberMixin")
        if not self.pk:
            try:
                last_department = self.__class__.objects.latest('pk')
                self.identification_number = "{:015d}".format(last_department.pk+1) + self.identification_number_ending
            except ObjectDoesNotExist:
                self.identification_number = "0" * 14 + "1" + self.identification_number_ending
        
        super().save(force_insert, force_update, using, update_fields)
