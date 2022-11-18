import pytest
from project.core.models import Cnpj, ConstraintError, Cpf, Customer, Identification, Registry


@pytest.mark.django_db
class TestCustomerModel:

    def test_model(self):
        ident = Cpf("11144477735")
        c = Customer.objects.create(identification=ident)

        assert c.pk
        assert type(c.identification) == Cpf
        assert c.identification == "11144477735"
        assert f"{c.identification:dot}" == "111.444.777-35"

    def test_factory(self):
        ident = Identification.of_kind("cpf", "11144477735")
        assert isinstance(ident, Cpf)

        ident = Identification.of_kind("cnpj", "01234567890123")
        assert isinstance(ident, Cnpj)

        with pytest.raises(TypeError):
            Identification.register("number", int)

        with pytest.raises(KeyError):
            Identification.of_kind("unknown", "somevalue")

    def test_registry(self):
        r = Registry()
        r.register("cpf", Cpf, country="BR", person="individual")
        r.register("cnpj", Cnpj, country="BR", person="business")

        assert r.get("cpf") is Cpf
        assert r.get("cnpj") is Cnpj
        assert r.filter(country="BR") == {Cpf, Cnpj}
        assert r.filter(person="individual") == {Cpf}
        assert r.filter(person="business") == {Cnpj}
        assert r.filter(country="US") == set()

        with pytest.raises(KeyError):
            r.register("cpf", Cpf)

        with pytest.raises(KeyError):
            r.get("unknown")

        with pytest.raises(ConstraintError):
            r.get("cpf", country="US")
