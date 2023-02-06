from abc import ABC, abstractmethod

from backend.dice import Die


class HitCalculator(ABC):
    @abstractmethod
    def get_attack_did_hit(self)->bool:
        raise NotImplementedError

    @abstractmethod
    def get_last_attack_did_crit(self)->bool:
        raise NotImplementedError


class AttackVsArmorClassHitCalculator(HitCalculator):
    def __init__(self, attack_bonus: int, armor_class: int)->None:
        self._atk_bonus=attack_bonus
        self._armor_class=armor_class
        self._last_result=None
        self._d20=Die(20)

    def get_attack_did_hit(self) ->bool:
        self._last_result=self._d20.roll()
        return (self._last_result==20 or (self._atk_bonus + self._last_result >= self._armor_class)) and not self._last_result==1

    def get_last_attack_did_crit(self) ->bool:
        return self._last_result==20

class SavingThrowHitCalculator(HitCalculator):
    def __init__(self, spell_save_dc: int = 13, saving_throw_modifier: int=0)-> None:
        self._saving_throw_modifier=saving_throw_modifier
        self._spell_save_dc=spell_save_dc
        self._d20=Die(20)

    def get_attack_did_hit(self) ->bool:
        return self._d20.roll()+self._saving_throw_modifier < self._spell_save_dc

    def get_last_attack_did_crit(self) ->bool:
        return False




class AlwaysHitNeverCrit(HitCalculator):
    def __init__(self):
        pass
    def get_last_attack_did_crit(self) ->bool:
        return False

    def get_attack_did_hit(self) ->bool:
        return True
