from typing import NamedTuple

import numpy as np

from backend.damage_calculator import DamageCalculator, AttackDamageCalculator
from backend.dice import Die
from backend.hit_calculator import HitCalculator, AttackVsArmorClassHitCalculator, AlwaysHitNeverCrit


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

    def get_damage_distribution(self, number_of_samples:int=50000) -> ScopeAndDistribution:
        attacks = number_of_samples
        damage = []
        for _n in range(attacks):
            damage.append(self.attack())
        diff_dmg = sorted(list(set(damage)))
        probabilities = []
        for dmg in diff_dmg:
            probabilities.append(damage.count(dmg) / attacks)

        return ScopeAndDistribution(np.array(diff_dmg),np.array(probabilities))


class EldritchBlast(AttackOption):
    def __init__(self, attack_bonus: int, armor_class:int, base_damage:int, number_of_attacks: int):
        hit_calculator = AttackVsArmorClassHitCalculator(attack_bonus=attack_bonus, armor_class=armor_class)
        damage_calculator = AttackDamageCalculator(dice=[Die(10)], base_damage=base_damage)
        super().__init__(hit_calculator, damage_calculator, number_of_attacks=number_of_attacks)

class FireBolt(AttackOption):
    def __init__(self, attack_bonus: int, armor_class: int, base_damage: int, number_of_dice: int):
        hit_calculator = AttackVsArmorClassHitCalculator(attack_bonus=attack_bonus, armor_class=armor_class)
        damage_calculator = AttackDamageCalculator(dice=[Die(10) for _n in range(number_of_dice)], base_damage=base_damage)
        super().__init__(hit_calculator, damage_calculator, number_of_attacks=1)

class ScorchingRay(AttackOption):
    def __init__(self, attack_bonus: int, armor_class:int, number_of_attacks:int=3):
        hit_calculator = AttackVsArmorClassHitCalculator(attack_bonus=attack_bonus, armor_class=armor_class)
        damage_calculator = AttackDamageCalculator(dice=[Die(6),Die(6)],
                                                   base_damage=0)
        super().__init__(hit_calculator, damage_calculator, number_of_attacks=number_of_attacks)

class MagicMissiles(AttackOption):
    def __init__(self, number_of_attacks: int = 3):
        hit_calculator=AlwaysHitNeverCrit()
        damage_calculator=AttackDamageCalculator(dice=[Die(4)], base_damage=1)
        super().__init__(hit_calculator, damage_calculator, number_of_attacks=number_of_attacks)