from attack_option import EldritchBlast, FireBolt
from interactive_plot import get_interactive_plot, get_interactive_plot_from_list


def test_interactive_plot()->None:
    get_interactive_plot()


def test_interactive_plot_from_list()->None:
    attacks=[EldritchBlast(7,17,4,2),FireBolt(7,17,4,2)]
    get_interactive_plot_from_list(attacks,'viridis')