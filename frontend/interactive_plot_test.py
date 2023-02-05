from backend.attack_option import EldritchBlast, FireBolt, MagicMissiles, ScorchingRay
from frontend.interactive_plot import get_interactive_plot_fire_bolt_vs_eldritch_blast, get_interactive_plot_from_list


def test_interactive_plot()->None:
    get_interactive_plot_fire_bolt_vs_eldritch_blast()



def test_interactive_plot_from_list()->None:
    attacks=[EldritchBlast(7,17,4,2),FireBolt(7,17,4,2),MagicMissiles(number_of_attacks=4),ScorchingRay(7,17)]
    get_interactive_plot_from_list(attacks,'viridis')