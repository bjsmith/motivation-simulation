__author__ = 'benjaminsmith'
import numpy as np
import time
import os
from copy import *
import matplotlib.pyplot as plt #we might do some other tool later.
from ActionModel import ActionModel
import sys
from BisbasModel import BisbasModel
from UnitModel import *


i_food = 0
i_friends = 1
i_partner = 2
i_study = 3


agents = [None,None]
for agent_i in [0,1]:
    agents[agent_i] = BisbasModel(
    states =
    [{"name":"Hunger", "value":1},
        {"name":"SocialNeed", "value":1},
        {"name":"RomanticNeed","value":1},
        {"name":"KnowledgeNeed","value":0.7}],
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
    baseline_action_threshold=2,
    learning_rate=0.05,
    action_tendency_persistence=1-0.08,
    satiation_power=0.05,
    consummatory_power=0.05,
    gains_v_losses=1)

    #model doesn't do anything: there's no environment elicitation. let's bring some food in.
    for e in agents[agent_i].elicitors:
        e.value=1.0

    agents[agent_i].actions[i_food].neg_expectancy=0.5
    agents[agent_i].actions[i_food].neg_val=0.5

    agents[agent_i].actions[i_study].neg_expectancy=0.72
    agents[agent_i].actions[i_study].neg_val=0.4

    #approaching a potential partner carries a high risk of rejection
    #while meeting friends carries very little negative but also lesser positive expected gain
    #partner
    agents[agent_i].actions[i_partner].pos_val=2
    agents[agent_i].actions[i_partner].pos_expectancy=2
    agents[agent_i].actions[i_partner].neg_val=4.0
    agents[agent_i].actions[i_partner].neg_expectancy=1.65
    #friend
    agents[agent_i].actions[i_friends].pos_val=0.8
    agents[agent_i].actions[i_friends].pos_expectancy=0.8
    agents[agent_i].actions[i_friends].neg_val=0.1
    agents[agent_i].actions[i_friends].neg_expectancy=0.1

    agents[agent_i].actions[i_friends].pos_expectancy=0.8
    agents[agent_i].actions[i_friends].neg_expectancy=0.4

    #sensible consummatory values.
    #   "approach potential partner" will exhaust the opportunity after one turn.
    agents[agent_i].action_elicitor[i_friends,i_friends]=0
    #   "meet friends" doesn't really get 'consumed' at all..
    agents[agent_i].action_elicitor[i_partner,i_partner]=1
    #studying also doesn't get 'consumed'.
    agents[agent_i].action_elicitor[i_study,i_study]=0

    #neither is the need satiated very quickly.
    agents[agent_i].action_state[i_study,i_study]=agents[agent_i].action_state[i_study,i_study]/4

#agents[0].step_and_display()
#agents[1].step_and_display()

#now...one of these individuals is more introverted: need for social interaction is satiated more quickly.
agents[1].action_state[i_friends,i_friends]=agents[1].action_state[i_friends,i_friends]*3

agents[0].gains_v_losses=0.95
for i in range(0,30):
    agents[0].step()
    agents[1].step()

    agents[0].display_current_state()
    plt.figure(agents[0].fig.number)

    agents[1].display_current_state()
    plt.figure(agents[1].fig.number)


    plt.pause(0.5)

agents[0].display_current_state_text()
agents[1].display_current_state_text()

print([a["actions"][i_friends].tendency for a in agents[0].record])
print([a["actions"][i_friends].tendency for a in agents[1].record])

print([a["actions"][i_food].tendency for a in agents[0].record])
[a["actions"][i_food].tendency for a in agents[1].record]

agents[0].states
agents[0].elicitors
