import numpy as np
import os
import matplotlib.pyplot as plt #we might do some other tool later.
from ActionModel import ActionModel
import collections as c
import traceback
from BisbasModel import BisbasModel
baseline_pos_expectancy=1
baseline_neg_expectancy=1
action_state_elicitations=10
# actions = [(ActionModel("Action" + str(i),0,0,baseline_pos_expectancy,baseline_neg_expectancy,1,1,1,0))
#                         for i in (range(1,action_state_elicitations+1))]

bb=BisbasModel(action_state_elicitations=4,
               baseline_pos_expectancy=1,
               baseline_neg_expectancy=1,
               baseline_action_threshold=4,
               learning_rate=0.1,
               action_tendency_persistence=0.9)

#keep it simple - map each action to the corresponding state

bb.consummatory_power = np.identity(len(bb.actions))/10
bb.actions[0].name="Eat"
bb.actions[1].name="Study"
bb.actions[2].name="Approach Partner"
bb.actions[3].name="Meet Friends"

bb.display_current_state_text()
bb.display_current_state()
#let's make the model hungry...
bb.states[0]=1.0
bb.step()
bb.display_current_state_text()

#model doesn't do anything: there's no environment elicitation. let's bring some food in.
bb.environment_elicitations[0]=1.0
bb.step()
bb.display_current_state_text()

#still nothing...because there's negative association with the action, it's not done.
#I'm not sure about including this reinforcement learning...
#anyhow, let's show the model that eating has a smaller negative than positive value.
bb.actions[0].neg_expectancy=0.5
bb.actions[0].neg_val=0.5

bb.step()
bb.display_current_state_text()

#OK. Now, we introduce a potential partner, friends, and also a study environment
bb.environment_elicitations[1]=1
bb.environment_elicitations[2] =1
bb.environment_elicitations[3] =1

#approaching a potential partner carries a high risk of rejection
#while meeting friends carries very little negative but also lesser positive expected gain
bb.actions[2].pos_val=2
bb.actions[2].pos_expectancy=2
bb.actions[2].neg_val=1.5
bb.actions[2].neg_expectancy=1.5

bb.actions[3].pos_val=0.8
bb.actions[3].pos_expectancy=0.8
bb.actions[3].neg_val=0.1
bb.actions[3].neg_expectancy=0.1


bb.step()
bb.display_current_state_text()

#still no desire...this is a flaw in the system - we need both appetite and reward expectancy
#which seems wrong somehow. Probably, gaining reward is itself an appetite we should include alongside the others.
#anyhow, let's set up some sexual and social appetite
bb.states[2]=1
bb.states[3]=1

bb.step()
bb.display_current_state_text()
#next task:
# we need to work out how to/whether to include a generalized "reward"-seeking parameter.
# also: if studying is actually motivated by an avoidance of failure, how do we model that?
# is that a good way to model this?
# how would we model the interaction of BIS/BAS in here in general...because we haven't really captured
# behavioral inhibition here, except given capacity for domain-specific inhibition.

#let's say participant has one bad *really* bad experience with approaching a partner
#reset states and environmental settings
for i in range(0,4):
    bb.states[i]=1
    bb.environment_elicitations[1]=1

#next time model approaches we're in for a shock.
bb.actions[2].neg_val=4
bb.step()
bb.display_current_state_text()

#it doesn't matter that next time there's no negative...damage is done!
bb.actions[2].neg_val=0
bb.step()
bb.display_current_state_text()

#OK so...maybe here's how to model reward:
#the learning process simply modifies learning weights that tie each behavior to each appetite based on past
#changes
#one 'appetite' can be pleasure or fun-seeking but this is just one among several, which happens to have
#potentially strong postive (and negative) payoffs from just about everything.

#this still doesn't tell us how to model the anxious person who studies because they want to avoid failing...

#list of supported import formats:
myval=5 # scalar
myval = [4,4,5] #list of numeric values
myval = {"One":1,"Two":2} #dictionary of numeric values.
#myval = [("One",1),("Two",2)] # we won't support tuples...seems unnecessary.
myval = [{"name":"One","value":1},{"name":"Two","value":2}] #do this first because it's our actual format.

object_type = "Action"
try:
    #OK, let's see if we can get the necessary values.
    necessary_vals = [{"name":e["name"],"value":e["value"]} for e in myval]
    #great! if this works, for a given input, then just pass out the *original* (allow for additional values to be loaded in)
    ret_val = myval
except TypeError as te:
    if(str(te)=="string indices must be integers, not str"):
        #seems that the iteration worked, but trying to get attributes didn't, indicating this isn't that kind of iterable.
        #let's try interpreting as a dictionary list of numeric values.
        ret_val = [{"name":k,"value":v} for k,v in myval.iteritems()]
    elif (str(te)=="'int' object has no attribute '__getitem__'"):
        #probably this is a list of numeric values.
        ret_val = [{"name":object_type + str(x),"value":i} for x,i in enumerate(myval)]
    elif (str(te)=="'int' object is not iterable"):
        ret_val = [{"name":object_type + str(i),"value":0} for i in range(0,myval)]
    else:
        ret_val=None
        raise

print(ret_val)

_ = [(k,v) for k,v in myval.iteritems()]

#rVal = c.OrderedDict(sorted(d.items(), key=lambda t: t[0]))

#constructor can be: scalar, iterable
#format is: list of dictionaries with values "name", "value"
try:
    #if it's an iterable
    _ = [e for e in myval]
    #yes...it's iterable
    try:#support a dictionary
        #OK, perhaps we *just have* the right format already.
        necessary_vals = [{"name"=e["name"],"name"=e["value"]} for e in myval]

            #necessary_vals = [{"name"=e.key,"name"=e.value} for e in myval]
        #but is it already in a specific order?
    except AttributeError:
        #OK, great, because we didn't really want dictionary format.
        #we wanted tuples. But they may have just passed a list.
        if all([len(i)==2 for i in myval]):
            #we have a tuple set.
            rVal = [(i[0],i[1]) for i in myval]
        else:#no tuples
            rVal = [(object_type + str(x),i) for x,i in enumerate(myval)]
            #more or less. still need to work out how we're gonna handle this given that Actions have been built with a whole bunch of stuff.
except TypeError:
    print "Was not an iterable."

#trying out np.dot
stateactions = np.diag((1,1,1))
stateactions[0,:]=1#make the first state output to every action
stateactions[:,0]=1#make the first action input from every state
states = [2,0,1]
np.dot(states,stateactions)
#OK so matrix multiplication between the weights and the values is what we want...
#let's integrate taht into the step function.

action_tendency_this = (
    np.array([a.pos_expectancy for a in bb.actions]) *
    np.dot([u.value for u in bb.states],bb.state_action) *
    np.dot([u.value for u in bb.elicitors],bb.elicitor_action) -
    np.array([a.neg_expectancy for a in bb.actions]) *
    np.dot([u.value for u in bb.states],bb.state_action) *
    np.dot([u.value for u in bb.elicitors],bb.elicitor_action)
    + np.array([a.tendency for a in bb.actions])*np.array([a.persistence for a in bb.actions]))


