__author__ = 'benjaminsmith'

import numpy as np
import time
import os
import matplotlib.pyplot as plt #we might do some other tool later.
from ActionModel import ActionModel
import sys
from BisbasROModel import BisbasROModel
from UnitModel import *
from scipy.stats import norm

i_pleasant_taste = 0
i_salt = 1
# i_food = 0
# i_friends = 1
# i_partner = 2
# i_study = 3
# i_fear_threat = 4

i_moderate_solution=0
i_strong_solution=1


def setup_base_ro_salt_rat_model():
    baseline_pos_expectancy=1
    baseline_neg_expectancy=0
    action_state_elicitations=10


    #Learning: positive feedback increases mood; negative feedback decreases it. Not sure how to implement this..
    satiation_power=0.04
    bb=BisbasROModel(
        states =
        [{"name":"PleasureNeed", "value":1},
            {"name":"SaltNeed", "value":1}],
        actions =
        UnitModel.GetLayerOfUnits([
            {"name":"Drink Moderate Salt Sln", "value":0},
            {"name":"Drink Strong Salt Sln", "value":0}]),
        elicitors =
        [{"name":"Moderate Salt Sln", "value":1},
            {"name":"Strong Salt Sln", "value":1}],
        baseline_pos_expectancy=0,
        baseline_neg_expectancy=0,
        baseline_action_threshold=0.001,
        learning_rate=0.1,
        action_tendency_persistence=0.0,
        satiation_power=satiation_power,
        consummatory_power=0.00,#should be >=0, <1.
        gains_v_losses=1
        #,action_tendency_function=norm.cdf
    )


    bb.set_display_settings(tendency_graph_width=0.05,state_graph_width=8.0)
    bb.display_current_state_text()
    #keep it simple - map each action to the corresponding state




    bb.action_state[i_moderate_solution,i_pleasant_taste]=0.0
    bb.action_state[i_strong_solution, i_pleasant_taste] = -0.6*satiation_power
    bb.action_state[i_moderate_solution, i_salt] = 0.5*satiation_power
    bb.action_state[i_strong_solution, i_salt] = 1*satiation_power

    # to start, let's set the expectancies to equal the actual values;
    # this way we essentially assume the model has already been trained.
    bb.actions[i_moderate_solution].pos_expectancy = \
        np.array([0.0,
         bb.action_state[i_moderate_solution, i_salt]])

    bb.actions[i_strong_solution].pos_expectancy = \
        np.array([0.0,
         bb.action_state[i_strong_solution, i_salt]])

    bb.actions[i_moderate_solution].neg_expectancy = \
        np.array([-bb.action_state[i_moderate_solution, i_pleasant_taste],
         0.0])

    bb.actions[i_strong_solution].neg_expectancy = \
        np.array([-bb.action_state[i_strong_solution, i_pleasant_taste],
         0.0])

    # bb.state_action[i_pleasant_taste,i_moderate_solution] = 0.5
    # bb.state_action[i_pleasant_taste, i_strong_solution] = -0.5
    # bb.state_action[i_salt, i_moderate_solution] =          0.5
    # bb.state_action[i_salt, i_strong_solution] =            1
    #A pavlovian association between [anticipated] pleasant taste and moderate solution
    #pavlovian association between [anticipated] unpleasant taste and the strong solution
    #this isn't quite right. I think what we really want is to set it in the "valence" scores. I don't know where this is....


    # for a in bb.actions:
    #     a.pos_expectancy =
    #     a.neg_expectancy = np.zeros(len(bb.states))



    return bb
