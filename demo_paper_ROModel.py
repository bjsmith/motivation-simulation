import matplotlib.pyplot as plt #we might do some other tool later.
from SimulationVisualization import *
import matplotlib
__author__ = 'benjaminsmith'
from SetupBaseROSaltRatModel import *
matplotlib.interactive(True)
model_timestamp='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())

model1 = setup_base_ro_salt_rat_model()

#first model showing within-subject changes.

def demo_oversatiation(model):

    base_hz=5

    model.states[i_salt].value = 1.0

    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10,hz=0.7)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10,hz=0.7)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10,hz=0.7)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10,hz=0.7)

    model.elicitors[i_moderate_solution].value = 0
    model.set_display_settings(graph_title="Removed Moderate salt option")
    model.step_and_display(5,hz=0.7)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10,hz=0.7)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10,hz=0.7)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10,hz=0.7)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10,hz=0.7)

    model.elicitors[i_moderate_solution].value = 1
    model.states[i_pleasant_taste].value = 0
    model.set_display_settings(graph_title="Removed pleasant taste craving")
    model.step_and_display(5,hz=0.7)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10,hz=0.7)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10,hz=0.7)

    model.states[i_salt].value = 1.0
    model.set_display_settings(graph_title="Status: Induced saliene deficiency")
    model.step_and_display(10,hz=0.7)

    model.states[i_salt].value = -1.0
    model.set_display_settings(graph_title="Status: Saliene injected")
    model.step_and_display(10,hz=0.7)

    return model

model1 = demo_oversatiation(model1)


graphplt=SimulationVisualization.graph_model_record_2(model1)
graphplt.savefig("demo_paper_ROModel"+ model_timestamp+".png")
print("finished.")
