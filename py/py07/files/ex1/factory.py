from ex0.factory import CreatureFactory
from ex1.creatures import Sproutling, Bloomelle, Shiftling, Morphagon


class HealingCreatureFactory(CreatureFactory):
    """Factory for healing-capable Creatures."""

    def create_base(self):
        return Sproutling()

    def create_evolved(self):
        return Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    """Factory for transform-capable Creatures."""

    def create_base(self):
        return Shiftling()

    def create_evolved(self):
        return Morphagon()
