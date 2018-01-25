import matplotlib.pyplot as plt #we might do some other tool later.
from SimulationVisualization import *
__author__ = 'benjaminsmith'
from SetupBaseSaltRatModel import *
#import Tkinter as tk

model1 = setup_base_salt_rat_model()

#first model showing within-subject changes.

def demo_oversatiation(model):
    base_hz=5

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10)

    model.states[i_pleasant_taste].value = 0
    model.set_display_settings(graph_title="Removed pleasant taste craving")
    model.step_and_display(5)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10)

    return model

model1 = demo_oversatiation(model1)

SimulationVisualization.graph_model_record_2(model1)

print("finished.")
