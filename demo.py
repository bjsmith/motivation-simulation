import numpy as np
import time
import os
import matplotlib.pyplot as plt #we might do some other tool later.
from ActionModel import ActionModel
from BisbasModel import BisbasModel
baseline_pos_expectancy=1
baseline_neg_expectancy=1
action_state_elicitations=10
# actions = [(ActionModel("Action" + str(i),0,0,baseline_pos_expectancy,baseline_neg_expectancy,1,1,1,0))
#                         for i in (range(1,action_state_elicitations+1))]

bb=BisbasModel.asSimpleModel(action_state_elicitations=4,
               baseline_pos_expectancy=1,
               baseline_neg_expectancy=1,
               baseline_action_threshold=3,
               learning_rate=0.1,
               action_tendency_persistence=0.9)

#keep it simple - map each action to the corresponding state

bb.action_elicitor = np.identity(len(bb.actions))/10
bb.action_state = np.identity(len(bb.actions))/10
bb.actions[0].name="Eat"
bb.actions[1].name="Study"
bb.actions[2].name="Approach Partner"
bb.actions[3].name="Meet Friends"
#bb.actions[4].name="Be Happy"


#let's make the model hungry...
bb.states[0].value=1.0
bb.states[1].value=1
bb.states[2].value=1
bb.states[3].value=1


bb.step()
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