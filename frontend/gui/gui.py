import inspect
import tkinter as tk
from functools import partial
from typing import Type

import matplotlib
from matplotlib import pyplot as plt

from backend.attack_option import AttackOption

INIT_OPTION: str = "Select an Option"
DEFAULT_PARAMS={"number_of_dice":1, "number_of_attacks":1, "base_damage": 0, "armor_class": 12, "attack_bonus": 3}

class FrontEndAttackOption:
    def __init__(self,master: tk.Tk,attack_option: Type[AttackOption], option_id: int)-> None:
        self.attack_option = attack_option
        self.option_id = option_id
        self.frame = tk.Frame(master, width=500)
        self.label = tk.Label(self.frame, text=attack_option.name)
        self.label.pack(side=tk.LEFT,padx=20)

        params = inspect.signature(attack_option.__init__).parameters
        params = [param for param in params if param != "self"]
        self.label_frame=tk.Frame(self.frame,width=500)
        self.entry_frame=tk.Frame(self.frame,width=500)
        self.entries = []
        for param in params:
            label = tk.Label(self.label_frame, width=20,text=param)
            entry = tk.Entry(self.entry_frame, width=20)
            if param in DEFAULT_PARAMS:
                entry.insert(0,DEFAULT_PARAMS[param])
            else:
                entry.insert(0, "0")
            self.entries.append(entry)
            label.pack(side=tk.RIGHT)
            self.entries[-1].pack(side=tk.RIGHT)
        self.label_frame.pack()
        self.entry_frame.pack()
        self.frame.pack()

    def get_attack_option(self)-> AttackOption:
        args=[]
        for entry in self.entries:
            tmp=int(entry.get())
            args.append(tmp)
        return self.attack_option(*args)



class MainWindow:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("1000x500")
        self.root.title("Plot configuration")
        # Create the list of options
        self.attack_options=AttackOption.__subclasses__()
        self.options_list = [attack_option.name for attack_option in self.attack_options]
        self.option_ids=[]
        # Variable to keep track of the option
        # selected in OptionMenu
        self.value_inside = tk.StringVar(self.root)

        # Set the default value of the variable
        self.value_inside.set(INIT_OPTION)

        # Create the optionmenu widget and passing
        # the options_list and value_inside to it.
        self.question_menu = tk.OptionMenu(self.root, self.value_inside, *self.options_list)
        self.question_menu.pack()
        buttons_frame=tk.Frame(self.root)

        add_button = tk.Button(buttons_frame,text="+",command=self.add_entry)
        add_button.pack(side=tk.LEFT)
        clear_button=tk.Button(buttons_frame,text="clear",command=self.clear)
        clear_button.pack(side=tk.RIGHT)
        buttons_frame.pack()
        self.front_end_attack_options: list[FrontEndAttackOption]=[]
        plot_button=tk.Button(self.root,text="plot", command=self.plot)
        plot_button.pack(side=tk.BOTTOM)


    def add_entry(self):
        value=self.value_inside.get()
        if value == INIT_OPTION:
            raise ValueError("No Attack Option set.")
        else:
            idx=self.options_list.index(value)
            if len(self.option_ids)>0:
                self.option_ids.append(self.option_ids[-1]+1)
            else:
                self.option_ids.append(0)
            self.front_end_attack_options.append(FrontEndAttackOption(self.root,self.attack_options[idx], self.option_ids[-1]))
            delete_button=tk.Button(self.front_end_attack_options[-1].frame,text="-",command=partial(self.clear_option_by_id,self.option_ids[-1]))
            delete_button.pack(side=tk.LEFT)


    def plot(self):
        plt.close()
        num_plots=len(self.front_end_attack_options)
        for idx,front_end_attack_option in enumerate(self.front_end_attack_options):
            color_float=idx/num_plots
            attack_option=front_end_attack_option.get_attack_option()
            scope, distribution=attack_option.get_damage_distribution()
            distribution*=100
            plt.plot(scope,distribution,color=matplotlib.colormaps["viridis"](color_float),linestyle="none",marker="x", label=attack_option.name)
        plt.legend()
        plt.ylabel("Probability [%]")
        plt.xlabel("Damage")
        plt.show()

    def clear(self)->None:
        for idx, option in enumerate(self.front_end_attack_options):
            option.frame.destroy()
        self.front_end_attack_options=[]

    def clear_option_by_id(self,option_id: int)->None:
        for idx, option in enumerate(self.front_end_attack_options):
            if option.option_id == option_id:
                option.frame.destroy()
                self.front_end_attack_options.pop(idx)
                break




    def print(self):
        print(self.value_inside.get())


if __name__=="__main__":
    pass