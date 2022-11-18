import pytest
from project.core.models import Customer, Cpf, Identification, Cnpj


@pytest.mark.django_db
class TestCustomerModel:

    def test_model(self):
        ident = Cpf("11144477735")
        c = Customer.objects.create(identification=ident)

        assert c.pk
        assert type(c.identification) == Cpf
        assert c.identification == "11144477735"
        assert f"{c.identification:.}" == "111.444.777-35"

    def test_factory(self):
        print(Identification.kinds)
        ident = Identification.of_kind("cpf", "11144477735")
        assert isinstance(ident, Cpf)

        ident = Identification.of_kind("cnpj", "01234567890123")
        assert isinstance(ident, Cnpj)
