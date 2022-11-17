from django.db import models


class IdentificationTypes(models.TextChoices):
    BRCPF = "BrCpf", "CPF"
    BRCNPJ = "BrCnpj", "CNPJ"
    BRRG = "BrRg", "RG"


class BadCustomer(models.Model):
    identification_value = models.CharField(max_length=256)
    identification_type = models.CharField(choices=IdentificationTypes.choices, max_length=32)


class Identification(str):
    pass


class Cpf(Identification):
    pass


class IdentificationField(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.field_value = models.CharField(max_length=256)
        self.field_type = models.CharField(max_length=32, choices=IdentificationTypes.choices)

        self.field_value_name = f"{self.name}_value"
        self.field_type_name = f"{self.name}_type"

    def contribute_to_class(self, cls, name, private_only=False):
        cls.add_to_class(self.field_type_name, self.field_type)
        cls.add_to_class(self.field_value_name, self.field_value)

    def __set__(self, instance, value):
        if not isinstance(value, Identification):
            raise TypeError(f"Expected type Identification, but received {type(value)}.")

        setattr(instance, self.field_value_name, str(value))
        setattr(instance, self.field_type_name, type(value).__name__)


class GoodCustomer(models.Model):
    identification = IdentificationField()
