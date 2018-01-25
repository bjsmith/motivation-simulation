import numpy as np
import sys
import matplotlib.pyplot as plt #we might do some other tool later.
from copy import *
from ActionROModel import ActionROModel
from UnitModel import UnitModel
import textwrap
from BisbasModel import BisbasModel
from scipy.stats import norm
import collections
import time
#see Python GUI (http://www.cosc.canterbury.ac.nz/greg.ewing/python_gui/)
#and http://insights.dice.com/2014/11/26/5-top-python-guis-for-2015/


class BisbasROModel(BisbasModel):
    #BisbasROModel differs from BisbasModel in that BisBasROModel doesn't have an independent reward value system that records value independently of consequences
    #BisbasModel will learn a target value of something entirely independent of the effects on interoceptive state;
    #BisbasROModel learns the effects on interoceptive state.
    #this default model assumes there's exactly one action for each state and exactly one thing that elicits each state
    #but other values can be passed.


    #a simple 1:1:1 model
    def __init__(self,
                 states,
                 actions,
                 elicitors,
                 baseline_pos_expectancy,
                 baseline_neg_expectancy,
                 baseline_action_threshold,
                 learning_rate,
                 action_tendency_persistence,
                 satiation_power,
                 consummatory_power,
                 gains_v_losses,
                 action_tendency_function=None
                 ):
        super().__init__(
                 states=states,
                 actions=actions,
                 elicitors=elicitors,
                 baseline_pos_expectancy=baseline_pos_expectancy,
                 baseline_neg_expectancy=baseline_neg_expectancy,
                 baseline_action_threshold=baseline_action_threshold,
                 learning_rate=learning_rate,
                 action_tendency_persistence=action_tendency_persistence,
                 satiation_power=satiation_power,
                 consummatory_power=consummatory_power,
                 gains_v_losses=gains_v_losses,
                 action_tendency_function=action_tendency_function
                 )

        self.actions = [ActionROModel(a.name,
                                    0,
                                    a.value,
                                    baseline_pos_expectancy, baseline_neg_expectancy,
                                    baseline_action_threshold,
                                    0,
                                    action_tendency_persistence)
                        for a in actions]

        # in the BisbasROModel, positive and negative expectancy learn the action_state relationships
        #pos_val and neg_val are pythonic PROPERTIES that simply denote positive and negative relationships within the action_state relationship

    def step(self,bb_record=[],silent=True):
        #this function steps one instant through running the model.
        #we need to figure out a good way to record progress of the model over time!

        print([a.value for a in self.actions])
        #calculate action tendency for the next timepoint
        print("used for action tendency:")
        print(self.actions)
        print(self.states)
        print(self.elicitors)

        #this function should be asking the question, "in context, what exactly reduces homeostatic state?"
        action_tendency_this = (
            self.action_tendency_function(
                np.dot([a.pos_expectancy for a in self.actions],[u.value for u in self.states]) *
                np.dot([u.value for u in self.elicitors],self.elicitor_action)
            ) -
            self.action_tendency_function(
                np.dot([a.neg_expectancy for a in self.actions],[u.value for u in self.states]) *
                np.dot([u.value for u in self.elicitors],self.elicitor_action) *
                self.gains_v_losses
            )
            + np.array([a.tendency for a in self.actions])*np.array([a.persistence for a in self.actions])
        )

        print("action_tendency_this:")
        print(action_tendency_this)
        #step through one full iteration of the model
        #calculate action tendencies for new round.
        #a fancier implementation should probably automatically copy the current state and then calculate everything
        #in next state from current state
        #this will do for now
        for i,action in enumerate(self.actions):
            assert isinstance(action, ActionROModel)
            self.actions[i].tendency = action_tendency_this[i]

                #for now, we haven't implemented a "fun-seeking" parameter which would build the model toward
                #optimizing the greatest reward regardless of possible pain. Partly because it seems like we ought to
                #have a corresponding "pain-avoidance" parameter, but I don't have theoretical justification for it.
                #also - would be nice to see if we can get it to emerge naturally somehow.
            #*then* set the action
            #reset action value
            self.actions[i].value=0

        #action tendencies are set. now act on one, if it crosses the threshold.
        #get the (first) maximum action tendency
        iter_ten=self.actions[0].tendency-1
        max_tendency_action=None

        for a in self.actions:
            if(a.tendency>iter_ten):
                iter_ten=a.tendency
                max_tendency_action=a

        if max_tendency_action.tendency>max_tendency_action.threshold:
            max_tendency_action.value=1
        else: max_tendency_action.value=0

        #now, the ACTUAL state response to the action
        state_change = np.dot([a.value for a in self.actions],self.action_state)
        pos_state_change = np.array([max(0, i) for i in state_change])
        neg_state_change = np.array([max(0, -i) for i in state_change])

        for j,state in enumerate(self.states):
            self.states[j].value-=state_change[j]

        #elicitor reponse to the action
        elicitor_change = np.dot([a.value for a in self.actions],self.action_elicitor)

        for j,elicitor in enumerate(self.elicitors):
            self.elicitors[j].value-=elicitor_change[j]
            if self.elicitors[j].value<0:
                self.elicitors[j].value=0

        #environment can't go below zero


        #nothing ventured, nothing-gained hypothesis- we only do learning on actions taken.
        # learning model
        #expected reward = expected reward_{t-1}*(1-learning_rate)+actual_reward*(l)
        for a in self.actions:
            if a.value==1.0:
                #learning rule.
                #actual change is going to be the change in internal state
                a.pos_expectancy = (
                    a.pos_expectancy*(1-self.learning_rate) +
                    pos_state_change*(self.learning_rate))
                print("learning rate:")
                print(self.learning_rate)
                print(a.pos_expectancy)
                #print(a.pos_val)
                #expected punishment = expected punishment_{t-1)*(1-learning_rate)+actual-reward*l
                #this would apply...if the reinforced value was negative, somehow.
                a.neg_expectancy = (
                    a.neg_expectancy*(1-self.learning_rate) +
                    neg_state_change*(self.learning_rate))
                #self.display_current_state_text()

        #an array was passed recording past values of bisBas model
        #add the current BisbasModel to it.
        #we can't *store* this in the Model itself because it would create recursive copies,
        #since we're using deep recursion. Will probably eventually need to code a kind of ModelSupervisor to handle
        #this kind of thing.

        #record the current state.
        self.record_current_values()









