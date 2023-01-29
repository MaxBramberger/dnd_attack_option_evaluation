from typing import NamedTuple

import numpy as np

from damage_calculator import DamageCalculator
from hit_calculator import HitCalculator

class ScopeAndDistribution(NamedTuple):
    scope: np.ndarray
    distribution: np.ndarray

class AttackOption:
    def __init__(self, hit_calculator: HitCalculator, damage_calculator: DamageCalculator, number_of_attacks: int =1)->None:
        self._damage_calculator=damage_calculator
        self._hit_calculator=hit_calculator
        self._number_of_attacks=number_of_attacks

    def attack(self)-> int:
        damage=0
        for _n in range(self._number_of_attacks):
            if self._hit_calculator.get_attack_did_hit():
                crit=self._hit_calculator.get_last_attack_did_crit()
                damage+=self._damage_calculator.get_damage(crit=crit)
        return damage

    def get_damage_distribution(self, number_of_samples=100000) -> ScopeAndDistribution:
        attacks = number_of_samples
        damage = []
        for n in range(attacks):
            damage.append(self.attack())
        diff_dmg = sorted(list(set(damage)))
        probabilities = []
        for dmg in diff_dmg:
            probabilities.append(damage.count(dmg) / attacks)

        return ScopeAndDistribution(np.array(diff_dmg),np.array(probabilities))

