from django.db import models
from rest_framework import serializers

from localflavors.ident import IdentificationFactory


class Customer(models.Model):
    identification_value = models.CharField(max_length=256)
    identification_kind = models.CharField(choices=IdentificationFactory.choices(), max_length=32)

    @property
    def identification(self):
        return IdentificationFactory.of_kind(self.identification_kind, self.identification_value)

    @identification.setter
    def identification(self, ident):
        self.identification_kind, self.identification_value = IdentificationFactory.unpack(ident)


class CustomerSerializer(serializers.ModelSerializer):
    identification = serializers.SerializerMethodField(method_name="identification_method")

    def identification_method(self, value):
        ...
        # of_kind
        # unpack
