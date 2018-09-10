import matplotlib.pyplot as plt #we might do some other tool later.
from SimulationVisualization import *
__author__ = 'benjaminsmith'
from SetupLearningSaltRatModel import *
#import Tkinter as tk



model1 = setup_learning_salt_rat_model()

model1.set_display_settings(tendency_graph_width=6, state_graph_width=8.0)

#first model showing within-subject changes.

def demo(model):
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

demo(model1)

SimulationVisualization.graph_model_record(model1)

print("finished.")


#possible designs:
# - on action, use the state change to calculate overall positive/negative change scores
# - modify the expected value vectors of environment and behavior neurons by making them more positive or more negative in response to the changes.
# - on action selecton