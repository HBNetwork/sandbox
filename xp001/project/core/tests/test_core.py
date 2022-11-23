import pytest

from localflavors.br import Cpf
from project.core.models import Customer


@pytest.mark.django_db
class TestCustomerModel:

    def test_model(self):
        ident = Cpf("11144477735")
        c = Customer.objects.create(identification=ident)

        assert c.pk
        assert type(c.identification) == Cpf
