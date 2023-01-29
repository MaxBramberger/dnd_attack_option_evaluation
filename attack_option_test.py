from matplotlib import pyplot as plt

from attack_option import AttackOption
from damage_calculator import AttackDamageCalculator
from dice import Die
from hit_calculator import AttackVsArmorClassHitCalculator


def test_eldritch_blast() -> None:
    hit_calculator=AttackVsArmorClassHitCalculator(attack_bonus=7, armor_class=17)
    damage_calculator=AttackDamageCalculator(dice=[Die(10)],base_damage=4)
    eldritch_blast=AttackOption(hit_calculator,damage_calculator,number_of_attacks=2)
    scope, distribution=eldritch_blast.get_damage_distribution()

    plt.plot(scope,distribution, "r+")
    plt.show()

def test_fire_bolt() -> None:
    hit_calculator=AttackVsArmorClassHitCalculator(attack_bonus=7, armor_class=17)
    damage_calculator=AttackDamageCalculator(dice=[Die(10),Die(10)],base_damage=4)
    fire_bolt=AttackOption(hit_calculator,damage_calculator,number_of_attacks=1)
    scope, distribution=fire_bolt.get_damage_distribution()

    plt.plot(scope,distribution, "b+")
    plt.show()

def test_eldritch_blast_vs_fire_bolt()-> None:
    hit_calculator=AttackVsArmorClassHitCalculator(attack_bonus=7, armor_class=17)
    damage_calculator=AttackDamageCalculator(dice=[Die(10)],base_damage=4)
    eldritch_blast=AttackOption(hit_calculator,damage_calculator,number_of_attacks=2)
    scope, distribution=eldritch_blast.get_damage_distribution()

    plt.plot(scope,distribution, "r+", label="eldritch blast")
    hit_calculator=AttackVsArmorClassHitCalculator(attack_bonus=7, armor_class=17)
    damage_calculator=AttackDamageCalculator(dice=[Die(10),Die(10)],base_damage=4)
    fire_bolt=AttackOption(hit_calculator,damage_calculator,number_of_attacks=1)
    scope, distribution=fire_bolt.get_damage_distribution()

    plt.plot(scope,distribution, "b+", label="fire bolt")
    plt.legend()
    plt.show()