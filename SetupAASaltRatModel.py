__author__ = 'benjaminsmith'

import numpy as np
import time
import os
import matplotlib.pyplot as plt #we might do some other tool later.
from ActionModel import ActionModel
import sys
from BisbasModel import BisbasModel
from UnitModel import *
from scipy.stats import norm

#i_pleasant_taste = 0
i_salt = 0
# i_food = 0
# i_friends = 1
# i_partner = 2
# i_study = 3
# i_fear_threat = 4

i_moderate_solution=0
i_strong_solution=1

#this model focuses on how pathways through "approach" and "avoid" can produce non-monotonic solutions

def setup_AA_salt_rat_model():
    baseline_pos_expectancy=1
    baseline_neg_expectancy=0
    action_state_elicitations=10


    #Learning: positive feedback increases mood; negative feedback decreases it. Not sure how to implement this..

    bb=BisbasModel(
        states =
        [{"name":"SaltNeed", "value":1}],
        actions =
        UnitModel.GetLayerOfUnits([
            {"name":"Drink Moderate Salt Sln", "value":0},
            {"name":"Drink Strong Salt Sln", "value":0}]),
        elicitors =
        [{"name":"Moderate Salt Sln", "value":1},
            {"name":"Strong Salt Sln", "value":1}],
        baseline_pos_expectancy=1,
        baseline_neg_expectancy=0,
        baseline_action_threshold=0.1,
        learning_rate=0.00,
        action_tendency_persistence=0.0,
        satiation_power=0.01,
        consummatory_power=0.00,#should be >=0, <1.
        gains_v_losses=1#,
        #action_tendency_function=norm.cdf
    )

    bb.set_display_settings(graph_width=8)
    bb.display_current_state_text()
    #keep it simple - map each action to the corresponding state


    #bb.action_state[i_moderate_solution,i_pleasant_taste]=0.0
    #bb.action_state[i_strong_solution, i_pleasant_taste] = 0.0
    bb.action_state[i_moderate_solution, i_salt]    =   0.5*0.1
    bb.action_state[i_strong_solution, i_salt]      =   1*0.1

    #bb.state_action[i_pleasant_taste,i_moderate_solution] = 0.5
    #bb.state_action[i_pleasant_taste, i_strong_solution] = -0.5
    bb.state_action[i_salt, i_moderate_solution]    =   1.0
    bb.state_action[i_salt, i_strong_solution]      =   1.0
    #A pavlovian association between [anticipated] pleasant taste and moderate solution
    #pavlovian association between [anticipated] unpleasant taste and the strong solution
    #this isn't quite right. I think what we really want is to set it in the "valence" scores. I don't know where this is....

    bb.actions[i_moderate_solution].pos_expectancy  =   0.5
    bb.actions[i_moderate_solution].neg_expectancy  =   0.0
    bb.actions[i_moderate_solution].pos_val = 0.5
    bb.actions[i_moderate_solution].neg_val = 0.0

    bb.actions[i_strong_solution].pos_expectancy = 0.5
    bb.actions[i_strong_solution].neg_expectancy = 0.2
    bb.actions[i_strong_solution].pos_val = 0.5
    bb.actions[i_strong_solution].neg_val = 0.2

    return bb
