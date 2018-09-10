import matplotlib.pyplot as plt #we might do some other tool later.
from SimulationVisualization import *
__author__ = 'benjaminsmith'
from SetupAASaltRatModel import *
#import Tkinter as tk

model1 = setup_AA_salt_rat_model()

model1.set_display_settings(state_graph_width=3,tendency_graph_width=1)
#first model showing within-subject changes.

def demo_oversatiation(model):

    base_hz=5

    #this time we are still interested in moderating the states.
    #but rather than having competing states (PleasureNeed vs. SaltNeed)
    #we have a single state (saltNeed).
    #the action is created by balancing approach/avoid.
    do_step = lambda n : model.step_and_display(n,0.7)
    #do_step = lambda n : model.step(n)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    do_step(10)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    do_step(10)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    do_step(10)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    do_step(10)

    # model.states[i_pleasant_taste].value = 0
    # model.set_display_settings(graph_title="Removed pleasant taste craving")
    # model.step_and_display(5)
    #
    # model.states[i_salt].value = 1.0
    # model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    # model.step_and_display(10)
    #
    # model.states[i_salt].value = -1.0
    # model.set_display_settings(graph_title="Status: Saliene injected")
    # model.step_and_display(10)
    #
    # model.states[i_salt].value = 1.0
    # model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    # model.step_and_display(10)
    #
    # model.states[i_salt].value = -1.0
    # model.set_display_settings(graph_title="Status: Saliene injected")
    # model.step_and_display(10)

    return model

model1 = demo_oversatiation(model1)

SimulationVisualization.graph_model_record_2(model1)
text = input("press return/enter to finish.")

