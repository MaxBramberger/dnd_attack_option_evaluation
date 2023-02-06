from typing import NamedTuple

import numpy as np

from backend.damage_calculator import DamageCalculator, AttackDamageCalculator
from backend.dice import Die
from backend.hit_calculator import HitCalculator, AttackVsArmorClassHitCalculator, AlwaysHitNeverCrit, \
    SavingThrowHitCalculator

CANTRIP_INTEGER_DICT={n : 1 if n <5 else 2 if n<11 else 3 if n<17 else 4 for n in range(1,21)}

class ScopeAndDistribution(NamedTuple):
    scope: np.ndarray
    distribution: np.ndarray

class AttackOption:
    name: str
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
    name: str = "Eldritch Blast"
    def __init__(self, attack_bonus: int, armor_class:int, base_damage:int, character_level: int=1):
        hit_calculator = AttackVsArmorClassHitCalculator(attack_bonus=attack_bonus, armor_class=armor_class)
        damage_calculator = AttackDamageCalculator(dice=[Die(10)], base_damage=base_damage)
        super().__init__(hit_calculator, damage_calculator, number_of_attacks=CANTRIP_INTEGER_DICT[character_level])

class FireBolt(AttackOption):
    name: str = "Fire Bolt"
    def __init__(self, attack_bonus: int, armor_class: int, base_damage: int, character_level: int =1):
        hit_calculator = AttackVsArmorClassHitCalculator(attack_bonus=attack_bonus, armor_class=armor_class)
        damage_calculator = AttackDamageCalculator(dice=[Die(10) for _n in range(CANTRIP_INTEGER_DICT[character_level])], base_damage=base_damage)
        super().__init__(hit_calculator, damage_calculator, number_of_attacks=1)

class ScorchingRay(AttackOption):
    name: str = "Scorching Ray"
    def __init__(self, attack_bonus: int, armor_class:int, spell_level:int=2):
        if spell_level < 2:
            raise ValueError("Scorching Ray needs to be cast at least on lvl 2.")
        hit_calculator = AttackVsArmorClassHitCalculator(attack_bonus=attack_bonus, armor_class=armor_class)
        damage_calculator = AttackDamageCalculator(dice=[Die(6),Die(6)],
                                                   base_damage=0)
        super().__init__(hit_calculator, damage_calculator, number_of_attacks=spell_level+1)

class MagicMissiles(AttackOption):
    name: str = "Magic Missiles"
    def __init__(self, spell_level: int = 1):
        hit_calculator=AlwaysHitNeverCrit()
        damage_calculator=AttackDamageCalculator(dice=[Die(4)], base_damage=1)
        super().__init__(hit_calculator, damage_calculator, number_of_attacks=spell_level+2)

class Disintegrate(AttackOption):
    name: str = "Disintegrate"

    def __init__(self,spell_save_dc: int = 13, saving_throw_modifier: int =0,spell_level: int =6):
        if spell_level < 6:
            raise ValueError("Disintegrate needs to be cast at least on lvl 6.")
        hit_calculator = SavingThrowHitCalculator(spell_save_dc,saving_throw_modifier)
        damage_calculator = AttackDamageCalculator(dice=[Die(6) for _n in range(10+3*(spell_level-6))],
                                                   base_damage=40)
        super().__init__(hit_calculator, damage_calculator, number_of_attacks=1)