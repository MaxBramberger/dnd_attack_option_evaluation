from abc import ABC, abstractmethod

from backend.dice import Die


class DamageCalculator(ABC):
    @abstractmethod
    def get_damage(self, crit: bool=False)-> int:
        raise NotImplementedError


class AttackDamageCalculator(DamageCalculator):

    def __init__(self, dice: list[Die], base_damage: int)->None:
        self._dice=dice
        self._base=base_damage

    def get_damage(self, crit: bool=False) -> int:
        damage=self._base
        for die in self._dice:
            damage+=die.roll()
            if crit:
                damage+=die.roll()
        return damage