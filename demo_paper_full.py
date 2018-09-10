import matplotlib.pyplot as plt #we might do some other tool later.
from SimulationVisualization import *
__author__ = 'benjaminsmith'
from SetupBaseStudentModel import *



#first model showing within-subject changes.
model1 = setup_base_student_model()
model1.set_display_settings(graph_width=3,tendency_graph_width=4)

def run_through_typical_study_day(model):
    # 1)	Role of Affordances
    # a.	Show how shift between absence and presence of friends will lead to changes from Studying to Hanging out.
    # b.	Start out with Environment: Presence of Friends and at the library, with high interoceptive state for nAff and moderately high for nACH.
    # b.	Start out with Environment: Presence of Friends and at the library, with high interoceptive state for nAff and moderately high for nACH.

    model.elicitors[i_food].value=0.0
    model.elicitors[i_friends].value=1.0
    model.elicitors[i_study].value=1.0

    while all([a.value==0 for a in model.actions]):
        model.step_and_display(1,1)

    for i in range(0,5):
        model.step_and_display(1,1)
    #SimulationVisualization.graph_model_record(model)

    #try to have this more obviously be leaving friends rather than getting bored of social situation.

    # c.	After several time steps have friends leave and watch shift in behavior.
    model.elicitors[i_friends].value=0.0

    while model.actions[i_study].value==0.0:
        model.step_and_display(1,1)

    for i in range(0,5):
        model.step_and_display(1,1)
    #SimulationVisualization.graph_model_record(model)


    # 2)	Role of Competition between alternative choices
    # a.	Show that given exactly the same settings, whether or not one Studies is a function of whether there is a strongly competing event, such as hunger and available food.
    # b.	Can take previous sequence and add Presence of Food and Hunger shortly after the Friends leave.
    #text from friend: free food giveaway in the student quad
    model.elicitors[i_food].value=1.0
    while model.actions[i_food].value==0.0:
        model.step_and_display(1,1)

    for i in range(0,15): #do 15 steps
        model.step_and_display(1,1)
    #SimulationVisualization.graph_model_record(model)

    #OK say there's another food giveaway
    model.elicitors[i_food].value=1.0

    for i in range(0,10):  #do 10 steps
        model.step_and_display(1,1)

    #this time the model still goes for the food, but spends very little time before returning to study.


    # 3)	Role of Interoceptive state
    # a.	Demo of how drop in interoceptive state, such as hunger or nAff will lead to shift to alternative behavior, such as Hanging out or Studying.
    #after a while studying, hunge returns
    model.states[i_food].value=1.0
    for i in range(0,10):  #do 10 steps
        model.step_and_display(1,1)



    # b.	After several cycles of eating, Hunger interoceptive state will drop and it will go back to Studying.
    for i in range(0,10):  #do 10 steps
        model.step_and_display(1,1)


    # 4)	Romantic partner
    # an attractive person walks into the study space and the individual wants to hit on them
    model.elicitors[i_partner].value=1.0
    for i in range(0,10):  #do 10 steps
        model.step_and_display(1,1)
    # because this opportunity is immediately 'consumed', i.e., after an approach, there's a result (rejection or not)
    # the model returns to studying behavior.


    return model

run_through_typical_study_day(model1)

SimulationVisualization.graph_model_record(model1)
# Individual differences
#we have an introvert.
#this is exactly the same as the model above; only difference (in this case) is that need for affiliation is
#satiated more quickly.
model2 = setup_base_student_model()
model2.action_state[i_friends,i_friends]=model2.action_state[i_friends,i_friends]*3
run_through_typical_study_day(model2)
SimulationVisualization.graph_model_record(model2)

#model3 is same as model1,but has a smaller appetite
model3 = setup_base_student_model()
model3.action_state[i_food,i_food]=model2.action_state[i_food,i_food]*3
run_through_typical_study_day(model3)
SimulationVisualization.graph_model_record(model3)
# 1)	rate of consummation
# a.	Show that how long you will Hang out with Friends before going back to studying is a function of amount of consummation per time step for nAff.
# 2)	differential gains for Approach and Avoidance
# a.	(May only work on Neural Network version).  Maybe could do something similar with gains and losses.
# b.	One possibility:  Set up situation in which Hangout or Studying is more activated than Leave, when Approach and Avoidance have the same gain.  Increase gain on Avoidance layer, and then show that Leave will be chosen over Hangout or Studying when gain reaches a certain level.
# 3)	Is there a way to model individual differences as differences in Baselineo levels of wanting or Interoceptive State?  Or can we make the Interoceptive system more sensitive?  I need to think about whether this can be done in the current system.
# 4)	Show differences in avoiding social rejection changes romantic partner behavior.

