import pytest
from project.core.models import GoodCustomer, BadCustomer, IdentificationTypes, Cpf, Identification, Cnpj


@pytest.mark.django_db
class TestCustomerModel:

    def test_with_metacolumn(self):
        id_type = IdentificationTypes.BRCPF
        id_value = "11144477735"
        c = BadCustomer.objects.create(identification_type=id_type, identification_value=id_value)

        assert c.pk
        assert c.identification_type == id_type
        assert c.identification_value == id_value

    def test_done_right(self):
        ident = Cpf("11144477735")
        c = GoodCustomer.objects.create(identification=ident)

        assert c.pk
        assert type(c.identification) == Cpf
        assert c.identification == "11144477735"

    def test_factory(self):
        ident = Identification.from_type("BrCpf", "11144477735")
        assert type(ident) == Cpf
        assert issubclass(Cpf, Identification)

        ident_cnpj = Identification.from_type("BrCnpj", "11144477735")
        assert type(ident_cnpj) == Cnpj
        assert issubclass(Cnpj, Identification)
