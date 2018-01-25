import matplotlib.pyplot as plt #we might do some other tool later.
from SimulationVisualization import *
__author__ = 'benjaminsmith'
from SetupBaseRatModel import *
import Tkinter as tk



#first model showing within-subject changes.
model1 = setup_base_rat_model()

def demo_craving(model):
    base_hz=2


    # 1)	Role of Affordances
    # a.	Show how shift between absence and presence of salt will lead to changes from Playing to Salt Consumption.
    # b.	Start out with Environment: Presence of Salt and at the RatPlayground, with high interoceptive state for needForSalt and moderately high for NeedForPlay.
    # b.	Start out with Environment: Presence of Salt and at the RatPlayground, with high interoceptive state for needforSalt and moderately high for NeedForPlay.
    model.elicitors[i_pleasant_taste].value=1.0
    model.elicitors[i_salt_need].value=1.0
    model.step_and_display(1, base_hz)
    print('starting..')
    for i in range(0,5):
        model.step_and_display(1,base_hz)
    #SimulationVisualization.graph_model_record(model)

    #can we simulate salt aversiveness after artificial injection of saliene?
    #this would have to be demonstrated by moving away from salt when one has consumed too much

    # tkRoot = tk.Tk()
    # myLabel = tk.Label(tkRoot, text="Injecting saliene! Watch what happens.")
    # myLabel.pack()
    # tkRoot.mainloop()
    # inject saliene
    model.states[i_salt].value = -0.5



    #model some more time going by
    model.step_and_display(10, base_hz)

    #after a while, saliene is important again
    model.states[i_salt].value = 1.0

    model.step_and_display(30, base_hz)

    return model

def demo_oversatiation(model):
    base_hz=2


    # 1)	Role of Affordances
    # a.	Show how shift between absence and presence of salt will lead to changes from Playing to Salt Consumption.
    # b.	Start out with Environment: Presence of Salt and at the RatPlayground, with high interoceptive state for needForSalt and moderately high for NeedForPlay.
    # b.	Start out with Environment: Presence of Salt and at the RatPlayground, with high interoceptive state for needforSalt and moderately high for NeedForPlay.
    model.elicitors[i_pleasant_taste].value = 1.0
    model.elicitors[i_salt_need].value = 2

    model.step_and_display(1, base_hz)
    print('starting..')
    for i in range(0,5):
        model.step_and_display(1,base_hz)
    #SimulationVisualization.graph_model_record(model)

    #can we simulate salt aversiveness after artificial injection of saliene?
    #this would have to be demonstrated by moving away from salt when one has consumed too much

    # tkRoot = tk.Tk()
    # myLabel = tk.Label(tkRoot, text="Injecting saliene! Watch what happens.")
    # myLabel.pack()
    # tkRoot.mainloop()
    # inject saliene
    model.states[i_salt_need].value = -0.5



    #model some more time going by
    model.step_and_display(10, base_hz)

    #after a while, saliene is important again
    model.states[i_salt_need].value = 1.0

    model.step_and_display(30, base_hz)

    return model

demo_oversatiation(model1)

demo_craving(model1)
SimulationVisualization.graph_model_record(model1)

print "finished."
