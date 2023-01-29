import matplotlib
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

from attack_option import EldritchBlast, AttackOption


def get_interactive_plot(color: str="red"):
    eldritch_blast=EldritchBlast(attack_bonus=7,armor_class=17,base_damage=4,number_of_attacks=2)
    scope, distribution=eldritch_blast.get_damage_distribution()
    fig=plt.figure()
    ax=fig.add_subplot(111)
    fig.subplots_adjust(left=0.25,bottom=0.25)
    line,=ax.plot(scope,distribution,marker="x", linestyle="none",color=color)

    atk_bonus_slider_ax = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=color)
    atk_bonus_slider = Slider(atk_bonus_slider_ax, 'Attack Bonus', 0.0, 19.0, valinit=7, valstep=1.)

    def sliders_on_changed(val):
        eldritch_blast = EldritchBlast(attack_bonus=int(atk_bonus_slider.val), armor_class=17, base_damage=4, number_of_attacks=2)
        scope, distribution = eldritch_blast.get_damage_distribution()
        line.set_data(scope,distribution)
        fig.canvas.draw_idle()
    atk_bonus_slider.on_changed(sliders_on_changed)
    plt.show()


def get_interactive_plot_from_list(attack_options:list[AttackOption],colormap_name: str="viridis"):
    default_params_num_attks={"attack_bonus":7,"armor_class":17,"base_damage":4,"number_of_attacks":2,}
    default_params_num_dice={"attack_bonus":7,"armor_class":17,"base_damage":4,"number_of_dice":2}
    for attack_option in attack_options:
        try:
            attack_option=type(attack_option)(**default_params_num_attks)
        except TypeError:
            attack_option = type(attack_option)(**default_params_num_dice)
    fig=plt.figure()
    ax=fig.add_subplot(111)
    fig.subplots_adjust(left=0.25,bottom=0.25)
    lines=[]
    for attack_option in attack_options:
        color_float=len(lines)/len(attack_options)
        scope,distribution=attack_option.get_damage_distribution()
        lines.append(ax.plot(scope,distribution,marker="x", linestyle="none",color=matplotlib.colormaps[colormap_name](color_float))[0])

    atk_bonus_slider_ax = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor="blue")
    atk_bonus_slider = Slider(atk_bonus_slider_ax, 'Attack Bonus', 0.0, 19.0, valinit=7, valstep=1.)
    def sliders_on_changed(val):
        default_params_num_dice["attack_bonus"]=int(atk_bonus_slider.val)
        default_params_num_attks["attack_bonus"]=int(atk_bonus_slider.val)
        for idx in range(len(attack_options)):
            try:
                attack_options[idx] = type(attack_options[idx])(**default_params_num_attks)
            except TypeError:
                attack_options[idx] = type(attack_options[idx])(**default_params_num_dice)
            scope, distribution = attack_options[idx].get_damage_distribution()
            lines[idx].set_data(scope,distribution)
        fig.canvas.draw_idle()
    atk_bonus_slider.on_changed(sliders_on_changed)
    plt.show()
