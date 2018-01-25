__author__ = 'benjaminsmith'

import numpy as np
import time
import os
import matplotlib.pyplot as plt #we might do some other tool later.
from ActionModel import ActionModel
import sys
from BisbasModel import BisbasModel
from UnitModel import *

i_food = 0
i_salt = 1
i_water = 2
i_play = 3
i_fear_threat = 4

# i_food = 0
# i_friends = 1
# i_partner = 2
# i_study = 3
# i_fear_threat = 4


def setup_base_rat_model():
    baseline_pos_expectancy=1
    baseline_neg_expectancy=1
    action_state_elicitations=10


    #Learning: positive feedback increases mood; negative feedback decreases it. Not sure how to implement this..

    bb=BisbasModel(
        states =
        [{"name":"Hunger", "value":0.99},
            {"name":"SaltNeed", "value":0.98},
            {"name":"WaterNeed","value":0.97},
            {"name":"PlayNeed","value":1},
            {"name":"Fear","value":0}],
        actions =
        UnitModel.GetLayerOfUnits([
            {"name":"EatProtein", "value":0},
            {"name":"EatSalt", "value":0},
            {"name":"Drink","value":0},
            {"name":"Play","value":0},
            {"name":"Flee from threat","value":0}]),
        elicitors =
        [{"name":"Food", "value":0},
            {"name":"Salt", "value":1},
            {"name":"Water","value":1},
            {"name":"RatPlayground","value":0},
            {"name":"Danger","value":0}],
        baseline_pos_expectancy=1,
        baseline_neg_expectancy=0,
        baseline_action_threshold=2,
        learning_rate=0.05,
        action_tendency_persistence=1-0.10,
        satiation_power=0.05,
        consummatory_power=0.0,#we can't ever run out of anything that exists. Food, water, salt supply is infinite
        gains_v_losses=1.5)

    bb.display_current_state_text()
    #keep it simple - map each action to the corresponding state

    # let's ignore negative expectancies for now.
    # #possibility of being injured while playing
    # bb.actions[i_play].neg_expectancy=0.1
    # bb.actions[i_play].neg_val=0.2

    #salt
    #let's ignore negative expectancies for now.
    bb.actions[i_salt].pos_val=1
    bb.actions[i_salt].neg_val=0
    bb.actions[i_salt].neg_expectancy=0


    #nothing negative happens while drinking water
    #water
    bb.actions[i_water].pos_val=1
    bb.actions[i_water].neg_val=0
    bb.actions[i_water].neg_expectancy=0


    #threat
    bb.actions[i_fear_threat].pos_val=4
    bb.actions[i_fear_threat].neg_val=0
    bb.actions[i_fear_threat].neg_expectancy=0


    #bb.action_state[i_play,i_play]=bb.action_state[i_play,i_play]/8

    #except for feear, which we won't model.
    #fleeing will quickly remove the threat.
    bb.action_elicitor[i_fear_threat,i_fear_threat]=0.5

    #but fear lasts a little longer.
    bb.action_state[i_fear_threat,i_fear_threat]=bb.action_state[i_fear_threat,i_fear_threat]*2

    return bb
