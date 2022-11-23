import pytest

from localflavors import IdentificationFactory
from localflavors.br import Cnpj, Cpf
from localflavors.registry import ConstraintError, Registry


class TestIdentifications:

    def test_cpf(self):
        ident = Cpf("11144477735")
        assert f"{ident:dot}" == "111.444.777-35"
        assert f"{ident:mask}" == "111.***.***-35"

    def test_factory(self):
        ident = IdentificationFactory.of_kind("cpf", "11144477735")
        assert isinstance(ident, Cpf)

        ident = IdentificationFactory.of_kind("cnpj", "01234567890123")
        assert isinstance(ident, Cnpj)

        with pytest.raises(KeyError):
            IdentificationFactory.of_kind("unknown", "somevalue")

        with pytest.raises(TypeError):
            IdentificationFactory.register("number", int)

        assert IdentificationFactory.choices() == [("cpf", "Cpf"), ("cnpj", "Cnpj")]

    def test_registry(self):
        r = Registry()
        r.register("cpf", Cpf, country="BR", person="individual")
        r.register("cnpj", Cnpj, country="BR", person="business")

        assert r["cpf"] == (Cpf, {("country", "BR"), ("person", "individual")})
        assert r["cnpj"] == (Cnpj, {("country", "BR"), ("person", "business")})
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

    def test_rationale(self):
        # self["cpf"] = (Cpf, {("country", "BR"), ("person", "individual")})
        r = {
            "cpf": (Cpf, {("country", "BR"), ("person", "individual")}),
            "cnpj": (Cnpj, {("country", "BR"), ("person", "business")}),
        }

        klass, registered_constraints = r["cpf"]
        assert {("country", "BR")}.issubset(registered_constraints)
