from localflavors.ident import Identification, IdentificationFactory, InvalidFormat


class CPFInvalid(InvalidFormat):
    pass


class Cpf(Identification):
    def __new__(cls, string):
        if not cls.checksum(string):
            raise CPFInvalid(string)

        return super().__new__(cls, string)

    def __format__(self, spec):
        if spec == "dot":
            return "{0}.{1}.{2}-{3}".format(self[:3], self[3:6], self[6:9], self[9:11])
        elif spec == "mask":
            return "{0}.***.***-{1}".format(self[:3], self[9:11])
        else:
            return self

    @staticmethod
    def checksum(value):
        """
        CPF Checksum algorithm.
        """

        def dv(partial):
            s = sum(b * int(v) for b, v in zip(range(len(partial) + 1, 1, -1), partial))
            return s % 11

        dv1 = 11 - dv(value[:9])
        q2 = dv(value[:10])
        dv2 = 11 - q2 if q2 >= 2 else 0

        return dv1 == int(value[9]) and dv2 == int(value[10])


class Cnpj(Identification):
    pass


IdentificationFactory.register(Cpf, country="BR", person="individual")
IdentificationFactory.register(Cnpj, country="BR", person="business")
