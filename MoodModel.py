import numpy as np
import time
import os
import matplotlib.pyplot as plt #we might do some other tool later.
from ActionModel import ActionModel
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
        {"name":"KnowledgeNeed","value":1},
        {"name":"Mood","value":1}],
    actions =
    UnitModel.GetLayerOfUnits([{"name":"Eat", "value":0},
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
    baseline_action_threshold=3,
    learning_rate=0.05,
    action_tendency_persistence=0.9)

bb.display_current_state_text()
#keep it simple - map each action to the corresponding state

#need to set up the relationships.
bb.state_action[range(0,4),:]=np.diag([1.0]*4)
bb.state_action[4,:]=[0.25,0.25,0.25,0.25] #should modify this study mood to be less.

#and the action_elicitor links.
bb.state_action[range(0,4),:]=np.diag([1.0]*4)
bb.state_action[4,:]=[0.25,0.25,0.25,0.25]
    #how much does each action satiate the "mood" item?
    #this really ought to depend on the amount of reward signal and we don't have a way to do that in the existing model
    #am I going down the wrong track?
    #not necessarily...but it's not going to entirely make sense until we make the reward signal into an associationist model
    #can we do that now or are there other more important things to sort out first?

########################################################################################################################

bb.step_and_display()
#model doesn't do anything: there's no environment elicitation. let's bring some food in.
bb.elicitors[0].value=1.0
bb.step()
bb.display_current_state()

#still nothing...because there's negative association with the action, it's not done.
#I'm not sure about including this reinforcement learning...
#anyhow, let's show the model that eating has a smaller negative than positive value.
bb.actions[0].neg_expectancy=0.5
bb.actions[0].neg_val=0.5

#bb.actions[1].pos_expectancy=2
#approaching a potential partner carries a high risk of rejection
#while meeting friends carries very little negative but also lesser positive expected gain
#partner
bb.actions[2].pos_val=2
bb.actions[2].pos_expectancy=2
bb.actions[2].neg_val=1.5
bb.actions[2].neg_expectancy=1.5
#friend
bb.actions[3].pos_val=0.8
bb.actions[3].pos_expectancy=1.6
bb.actions[3].neg_val=0.1
bb.actions[3].neg_expectancy=0.1

bb.actions[3].pos_expectancy=0.8
bb.actions[3].neg_expectancy=0.4

while bb.actions[0].value==0:
    bb.step()
    plt.pause(0.25)
    bb.display_current_state()

bb.step()
bb.display_current_state()

#OK. Now, we introduce a potential partner, friends, and also a study environment
bb.elicitors[1].value=1
bb.elicitors[2].value =1
bb.elicitors[3].value =1




bb.display_current_state()


bb.step()
bb.display_current_state()
#next task:
# we need to work out how to/whether to include a generalized "reward"-seeking parameter.
# also: if studying is actually motivated by an avoidance of failure, how do we model that?
# is that a good way to model this?
# how would we model the interaction of BIS/BAS in here in general...because we haven't really captured
# behavioral inhibition here, except given capacity for domain-specific inhibition.

#let's say participant has one bad *really* bad experience with approaching a partner
#reset states and environmental settings
for i in range(0,4):
    bb.elicitors[1].value=1

#next time model approaches we're in for a shock.
bb.actions[2].neg_val=4
bb.display_current_state()

while bb.actions[2].value==0:

    bb.step()
    bb.display_current_state()
    plt.pause(2)
bb.step()
bb.display_current_state()
bb.step()
bb.display_current_state()


#it doesn't matter that next time there's no negative...damage is done!
for i in range(0,10):
    bb.actions[2].neg_val=0
    bb.step()
    bb.display_current_state()
    plt.pause(2)