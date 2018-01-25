import matplotlib.pyplot as plt #we might do some other tool later.
from SimulationVisualization import *
__author__ = 'benjaminsmith'
from SetupBaseSaltRatModel import *
import Tkinter as tk



model1 = setup_base_salt_rat_model()
#first model showing within-subject changes.


def demo_oversatiation(model):
    base_hz=5

    model.set_display_settings(graph_title="Status: Saliene deficient")
    model.step_and_display(1, base_hz)
    print('starting..')
    for i in range(0,5):
        model.step_and_display(1,base_hz)
    #SimulationVisualization.graph_model_record(model)

    #can we simulate salt aversiveness after artificial injection of saliene?
    #this would have to be demonstrated by moving away from salt when one has consumed too much

    # inject saliene
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.states[i_salt].value = -0.5



    #model some more time going by
    model.step_and_display(10, base_hz)

    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    #after a while, saliene is important again
    model.states[i_salt].value = 1.0

    model.step_and_display(20, base_hz)

    return model

demo_oversatiation(model1)

SimulationVisualization.graph_model_record(model1)

print "finished."
