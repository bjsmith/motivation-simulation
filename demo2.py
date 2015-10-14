import numpy as np
import time
import os
import matplotlib.pyplot as plt #we might do some other tool later.
from ActionModel import ActionModel
import sys
from BisbasModel import BisbasModel
from UnitModel import *
baseline_pos_expectancy=1
baseline_neg_expectancy=1
action_state_elicitations=10


#for this model we're going to try build a model which has an explicit desire to seek positive feedback.
#So we're going to make "mood" an extra Need.
#There's no explicit Elicitor for mood, but various elicitors will elicit it to varying degrees.
#actually, we can't do this under the current model because there's no explicit connection between state and elicitors
#only each of their independent connections to actions.
#Mood competes as a Internal State like everything else...
#There's no explicit Action associated with Mood, but most actions have some effect on it.
#Learning: positive feedback increases mood; negative feedback decreases it. Not sure how to implement this..

#let's start with a model similiar to the last but with just one extra State, Mood.

bb=BisbasModel(
    states =
    [{"name":"Hunger", "value":1},
        {"name":"SocialNeed", "value":1},
        {"name":"RomanticNeed","value":1},
        {"name":"KnowledgeNeed","value":0.7}],
    actions =
    UnitModel.GetLayerOfUnits([
        {"name":"Eat", "value":0},
        {"name":"Meet friends", "value":0},
        {"name":"Approach potential partner","value":0},
        {"name":"Study","value":0}]),
    elicitors =
    [{"name":"Food", "value":0},
        {"name":"Friends", "value":0},
        {"name":"Potential partner","value":0},
        {"name":"Library","value":0}],
    baseline_pos_expectancy=1,
    baseline_neg_expectancy=1,
    baseline_action_threshold=2,
    learning_rate=0.05,
    action_tendency_persistence=1-0.08,
    satiation_power=0.05,
    consummatory_power=0.05,
    gains_v_losses=0.8)

bb.display_current_state_text()
#keep it simple - map each action to the corresponding state

print(UnitModel.get_list_names(bb.actions))
i_food = 0
i_friends = 1
i_partner = 2
i_study = 3
#model doesn't do anything: there's no environment elicitation. let's bring some food in.
bb.elicitors[i_food].value=1.0

bb.actions[i_food].neg_expectancy=0.25
bb.actions[i_food].neg_val=0.25

bb.actions[i_study].neg_expectancy=0.36
bb.actions[i_study].neg_val=0.2
bb.display_current_state()

#approaching a potential partner carries a high risk of rejection
#while meeting friends carries very little negative but also lesser positive expected gain
#partner
bb.actions[i_partner].pos_val=2
bb.actions[i_partner].pos_expectancy=2
bb.actions[i_partner].neg_val=2.0
bb.actions[i_partner].neg_expectancy=0.825
#friend
bb.actions[i_friends].pos_val=0.8
bb.actions[i_friends].pos_expectancy=0.8
bb.actions[i_friends].neg_val=0.05
bb.actions[i_friends].neg_expectancy=0.05

bb.actions[i_friends].pos_expectancy=0.8
bb.actions[i_friends].neg_expectancy=0.2

#sensible consummatory values.
#   "approach potential partner" will exhaust the opportunity after one turn.
bb.action_elicitor[i_friends,i_friends]=0
#   "meet friends" doesn't really get 'consumed' at all..
bb.action_elicitor[i_partner,i_partner]=1
#studying also doesn't get 'consumed'.
bb.action_elicitor[i_study,i_study]=0

#neither is the need satiated very quickly.
bb.action_state[i_study,i_study]=bb.action_state[i_study,i_study]/4

bb.display_current_state()

while bb.actions[0].value==0:
    bb.step_and_display(1,2)
    #OK. In order to do copy we're going to have to copy the individual attributes. Otherwise we're currently capturing graph objects and things and that's causing problems.

print("tendency increasing over time:")
print([iter["actions"][0].tendency for iter in bb.record])

bb.step_and_display()

#OK. Now, we introduce a potential partner, friends, and also a study environment
bb.elicitors[i_friends].value=1
bb.elicitors[i_partner].value =1
bb.elicitors[i_study].value =1

bb.step_and_display()

#next task:

#next time model approaches we're in for a shock.
bb.actions[i_partner].neg_val=4
bb.display_current_state()

while bb.actions[2].value==0:
    bb.step()
    bb.display_current_state()
    plt.pause(0.5)
bb.step_and_display(2,0.5)

#it doesn't matter that next time there's no negative...damage is done!
for i in range(0,5):
    bb.actions[2].neg_val=0
    bb.step()
    bb.display_current_state()
    plt.pause(0.5)

#take away other options, finally study happens.
for e in bb.elicitors:
    if e.name=="Food":
        e.value=0.0
    elif e.name=="Friends":
        e.value=0.0
    elif e.name=="Potential partner":
        e.value=0.0
for s in bb.states:
    if e.name=="SocialNeed":
        e.value=1.0
bb.step_and_display(30,5)

#OK. Let's say the individual is hungry again.
bb.states[i_food].value=1.0
bb.elicitors[i_food].value=1.0
bb.step_and_display(20,5)
