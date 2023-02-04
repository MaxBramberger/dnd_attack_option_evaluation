import inspect

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

from attack_option import EldritchBlast, AttackOption, FireBolt


def get_interactive_plot_fire_bolt_vs_eldritch_blast(color: str= "red"):
    eldritch_blast=EldritchBlast(attack_bonus=7,armor_class=17,base_damage=4,number_of_attacks=2)
    fire_bolt=FireBolt(attack_bonus=7,armor_class=17,base_damage=4,number_of_dice=2)
    scope, distribution=eldritch_blast.get_damage_distribution()
    distribution*=100
    scope2, distribution2=fire_bolt.get_damage_distribution()
    distribution2 *= 100
    fig=plt.figure()
    ax=fig.add_subplot(111)
    fig.subplots_adjust(left=0.25,bottom=0.25)
    line,=ax.plot(scope,distribution,marker="x", linestyle="none",color=color, label="Eldritch Blast")
    line2,=ax.plot(scope2,distribution2,marker="x",linestyle="none",color="blue", label="Fire Bolt")
    plt.title("Base dmg: 4, AC: 17, number of dice/attacks: 2")
    plt.ylabel(r"Probability [%]")
    plt.xlabel("Damage")
    plt.legend()

    atk_bonus_slider_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=color)
    atk_bonus_slider = Slider(atk_bonus_slider_ax, 'Attack Bonus', 0.0, 19.0, valinit=7, valstep=1.)

    def sliders_on_changed(val):
        eldritch_blast = EldritchBlast(attack_bonus=int(atk_bonus_slider.val), armor_class=17, base_damage=4, number_of_attacks=2)
        scope, distribution = eldritch_blast.get_damage_distribution()
        distribution *= 100
        line.set_data(scope,distribution)
        fire_bolt = FireBolt(attack_bonus=int(atk_bonus_slider.val), armor_class=17, base_damage=4,
                                       number_of_dice=2)
        scope, distribution = fire_bolt.get_damage_distribution()
        distribution *= 100
        line2.set_data(scope, distribution)
        fig.canvas.draw_idle()
    atk_bonus_slider.on_changed(sliders_on_changed)
    plt.show()


def get_interactive_plot_from_list(attack_options:list[AttackOption],colormap_name: str="viridis"):
    raise NotImplementedError("Flexible Plot is buggy, does currently not show.")
    params_all={"attack_bonus":7,"armor_class":17,"base_damage":4,"number_of_attacks":2,"number_of_dice":2}
    for attack_option in attack_options:
        signature=inspect.signature(type(attack_option).__init__)
        params=[param for param in signature.parameters if param !="self"]
        args={param: params_all[param] for param in params}
        attack_option=type(attack_option)(**args)

    fig=plt.figure()
    ax=fig.add_subplot(111)
    fig.subplots_adjust(left=0.25,bottom=0.25)
    lines=[]
    means=[]
    for attack_option in attack_options:
        color_float=len(lines)/len(attack_options)
        scope,distribution=attack_option.get_damage_distribution()
        lines.append(ax.plot(scope,distribution,marker="x", linestyle="none",label=str(type(attack_option)).split('.')[-1].split("'")[0],color=matplotlib.colormaps[colormap_name](color_float))[0])
        means.append(ax.plot(np.sum(scope*distribution)*np.ones(2),[0,0.4],color=matplotlib.colormaps[colormap_name](color_float),marker='o', mfc='none')[0])
    plt.legend()
    atk_bonus_slider_ax = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor="blue")
    atk_bonus_slider = Slider(atk_bonus_slider_ax, 'Attack Bonus', 0.0, 19.0, valinit=7, valstep=1.)
    ac_slider_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor="blue")
    ac_slider = Slider(ac_slider_ax, 'Armor Class', 0.0, 30.0, valinit=17, valstep=1.)
    base_damage_ax = fig.add_axes([0.25, 0.05, 0.65, 0.03], facecolor="blue")
    base_damage_slider = Slider(base_damage_ax, 'Base Damage', 0.0, 30.0, valinit=4, valstep=1.)
    def sliders_on_changed(val):
        params_all["attack_bonus"]=int(atk_bonus_slider.val)
        params_all["armor_class"] = int(ac_slider.val)
        params_all["base_damage"] = int(base_damage_slider.val)
        for idx in range(len(attack_options)):
            color_float = idx / len(attack_options)
            signature = inspect.signature(type(attack_options[idx]).__init__)
            params = [param for param in signature.parameters if param!="self"]
            args = {param: params_all[param] for param in params}
            attack_options[idx] = type(attack_options[idx])(**args)
            scope, distribution = attack_options[idx].get_damage_distribution()
            lines[idx].set_data(scope,distribution)
            means[idx].set_data(np.sum(scope*distribution)*np.ones(2),[0,0.4])
        fig.canvas.draw_idle()
    atk_bonus_slider.on_changed(sliders_on_changed)
    ac_slider.on_changed(sliders_on_changed)
    base_damage_slider.on_changed(sliders_on_changed)
    plt.show()
