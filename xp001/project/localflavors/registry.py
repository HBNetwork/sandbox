class ConstraintError(Exception):
    pass


class Registry(dict):
    def get(self, key, **constraints):
        constraints = frozenset(constraints.items())
        klass, registered_constraints = self[key]

        if not constraints.issubset(registered_constraints):
            raise ConstraintError(f"Key {key} is mapped to {klass} but the constraints {constraints} does not match.")

        return klass

    def filter(self, **constraints):
        constraints = frozenset(constraints.items())

        return {klass for klass, registered_constraints in self.values()
                if constraints.issubset(registered_constraints)}

    def register(self, key, klass, **constraints):
        if key in self:
            raise KeyError(f"Key {key} already exists.")

        self[key] = klass, frozenset(constraints.items())
