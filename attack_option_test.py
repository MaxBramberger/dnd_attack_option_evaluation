from matplotlib import pyplot as plt

from attack_option import AttackOption, EldritchBlast, FireBolt
from damage_calculator import AttackDamageCalculator
from dice import Die
from hit_calculator import AttackVsArmorClassHitCalculator


def test_eldritch_blast() -> None:
    eldritch_blast=EldritchBlast(attack_bonus=7,armor_class=17,base_damage=4,number_of_attacks=2)
    scope, distribution=eldritch_blast.get_damage_distribution()

    plt.plot(scope,distribution, "r+")
    plt.show()

def test_fire_bolt() -> None:
    fire_bolt=FireBolt(attack_bonus=7,armor_class=17,base_damage=4,number_of_dice=2)
    scope, distribution=fire_bolt.get_damage_distribution()

    plt.plot(scope,distribution, "b+")
    plt.show()

def test_eldritch_blast_vs_fire_bolt()-> None:
    eldritch_blast=EldritchBlast(attack_bonus=7,armor_class=17,base_damage=4,number_of_attacks=2)
    scope, distribution=eldritch_blast.get_damage_distribution()
    plt.plot(scope,distribution, "r+", label="eldritch blast")

    fire_bolt=FireBolt(attack_bonus=7,armor_class=17,base_damage=4,number_of_dice=2)
    scope, distribution=fire_bolt.get_damage_distribution()
    plt.plot(scope,distribution, "b+", label="fire bolt")
    plt.legend()
    plt.xlabel("Damage")
    plt.ylabel("Probability")
    plt.show()