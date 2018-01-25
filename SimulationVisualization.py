from SimulationVisualization import *
from SetupBaseSaltRatModel import *

import matplotlib as mpl
import matplotlib.pyplot as plt #we might do some other tool later.
import numpy as np
from matplotlib.font_manager import FontProperties

#import Tkinter as tk


from BisbasModel import *
import datetime
__author__ = 'benjaminsmith'

class SimulationVisualization(object):
    @classmethod
    def graph_model_record(cls,model):

        assert isinstance(model,BisbasModel)
        #model = bb
        dpi=80
        fig_height=8.0
        fig_width = 10.0
        my_cols = ['r','b','#009900','#999900','#990099']

        states_values = [[state.value for state in tp['states']] for tp in model.record]
        elicitor_values = [[elicitor.value for elicitor in tp['elicitors']] for tp in model.record]
        action_tendencies = [[action.tendency for action in tp['actions']] for tp in model.record]
        def get_active_action_name(a_set):
            for a in a_set:
                if a.value==1:
                    return a.name
            return None

        def get_active_action_index(a_set):
            for i, a in enumerate(a_set):
                if a.value==1:
                    return i
            return -1
        #action_values = [[i for i, action in enumerate(tp['actions']) if action.value!=0 else -1][0] for tp in model.record]
        action_values =[get_active_action_name(tp['actions']) for tp in model.record]
        action_values_i =[get_active_action_index(tp['actions']) for tp in model.record]

        #get points of change in action values.
        ap2 = action_values[1:len(action_values)]
        ap2.append(action_values[0])
        action_value_change = [i+1 for i, (j, k) in enumerate(zip(action_values, ap2)) if k!=j]
        action_value_change_v = [k for i, (j, k) in enumerate(zip(action_values, ap2)) if j!=k]

        scale = lambda val,scale,offset:[[x /scale + offset for x in y]for y in val]
        y_vals = range(0,len(states_values))
        fig, ax = plt.subplots(1,1, dpi=dpi,figsize=(fig_width,fig_height))

        y_pos_elicitor = 0.0
        y_pos_states=0.2
        y_pos_action_ten=0.4
        y_pos_action_values=0.9



        for p in range(0,len(states_values[0])):
            states_plot=ax.plot(y_vals,[s[p] for s in scale(states_values,10,y_pos_states)],label=model.record[0]['states'][p].name
                                ,color=my_cols[p])
            elicitors_plot = ax.plot(y_vals,[e[p] for e in scale(elicitor_values,10,y_pos_elicitor)],color=my_cols[p])
            at_plot = ax.plot(y_vals,[a[p] for a in scale(action_tendencies,20,y_pos_action_ten)],color=my_cols[p])

        #plt.legend(loc=5)

        fontP = FontProperties()
        fontP.set_size('small')
        #plt.legend([plt], "title", prop = fontP)
        #plt.legend(loc=3, prop=fontP)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=3, mode="expand", borderaxespad=0.,
                   prop=fontP
                   )
        plt.yticks([y_pos_action_ten+0.05,y_pos_elicitor+0.05,y_pos_states+0.05,y_pos_action_values+0.05],
                   ["Action Tendency","Elicitor","States","Action"])
        plt.ylim(0,1)

        #get the data for what the actions are at each point.

        #
        # #OK: let's try a color bar for the Actions. Then we can overlay text after.
        # cmap = mpl.cm.get_cmap()# plt.set_cmap
        # cmap.set_over('0.25')
        # cmap.set_under('0.75')
        #
        # # If a ListedColormap is used, the length of the bounds array must be
        # # one greater than the length of the color list.  The bounds must be
        # # monotonically increasing.
        ax_main_pos = ax.get_position()
        ax_actions = fig.add_axes([ax_main_pos.x0, 0.8, ax_main_pos.width, 0.05])
        ax_actions.imshow([action_values_i,action_values_i,action_values_i]
                          ,interpolation='none',
                          )
        ax_actions.set_xticks(action_value_change)
        ax_actions.yaxis.set_visible(False)

        ax_actions.set_xticklabels(action_value_change_v,rotation="vertical")
        ax_main_pos.colormap = mpl.colors.ListedColormap(my_cols)

        # #bounds = [0, 3, 4, 7, 8]
        # bounds = action_values
        # norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        # cb2 = mpl.colorbar.ColorbarBase(ax_actions, cmap=cmap,
        #                                      norm=norm,
        #                                      # to use 'extend', you must
        #                                      # specify two extra boundaries:
        #                                      boundaries=bounds,
        #                                      #extend='both',
        #                                      ticks=bounds, # optional
        #                                      spacing='proportional',
        #                                      orientation='horizontal')
        # cb2.set_label('Discrete intervals, some other units')
        # #add the states
        #
        # ax2=ax.twinx()
        # ax3=ax.twinx()
        # #add the elicitors
        # [tp['elicitors'] for tp in model.record]
        # #add the action tendencies
        # #add the actions
        # #add the rewards

    @classmethod
    def graph_model_record_2(cls,model):

        dpi = 80
        fig_height = 8.0
        fig_width = 10.0
        my_cols = ['r', 'b', '#009900', '#333333', '#000099']

        states_values = [[state.value for state in tp['states']] for tp in model.record]
        elicitor_values = [[elicitor.value for elicitor in tp['elicitors']] for tp in model.record]
        action_tendencies = [[action.tendency for action in tp['actions']] for tp in model.record]

        def get_active_action_name(a_set):
            for a in a_set:
                if a.value == 1:
                    return a.name
            return None

        def get_active_action_index(a_set):
            for i, a in enumerate(a_set):
                if a.value == 1:
                    return i
            return -1

        # action_values = [[i for i, action in enumerate(tp['actions']) if action.value!=0 else -1][0] for tp in model.record]
        action_values = [get_active_action_name(tp['actions']) for tp in model.record]
        action_values_i = [get_active_action_index(tp['actions']) for tp in model.record]

        # get points of change in action values.
        ap2 = action_values[1:len(action_values)]
        ap2.append(action_values[0])
        action_value_change = [i + 1 for i, (j, k) in enumerate(zip(action_values, ap2)) if k != j]
        action_value_change_v = [k for i, (j, k) in enumerate(zip(action_values, ap2)) if j != k]

        scale = lambda val, scale, offset: [[x / scale + offset for x in y] for y in val]
        y_vals = range(0, len(states_values))

        y_pos_elicitor = 0.0
        y_pos_states = 0.2
        y_pos_action_ten = 0.4
        y_pos_action_values = 0.9

        # fig, ax = plt.subplots(1,1, dpi=dpi,figsize=(fig_width,fig_height))
        fig, ax_list = plt.subplots(4, 1, dpi=dpi,
                                    figsize=(fig_width, fig_height))  # a figure with a 4x1 grid of axes


        ax_list[0].set_title("States")
        ax_list[1].set_title("Elicitors")
        ax_list[2].set_title("Action Tendencies")
        ax_list[3].set_title("Actions")

        plt.tight_layout()
        for p in [0,1,2]:
            ax_list[p].set_color_cycle(my_cols)
            ax_list[p].axhline(y=0, linestyle="dashed", color="#999999")

        for p in range(0, len(states_values[0])):
            states_plot = ax_list[0].plot([x[p] for x in states_values],label=UnitModel.get_list_names(model.states)[p],linewidth=2)
        for p in range(0, len(elicitor_values[0])):
            elicitors_plot = ax_list[1].plot([x[p] for x in elicitor_values],label=UnitModel.get_list_names(model.elicitors)[p],linewidth=2)
        for p in range(0, len(action_tendencies[0])):
            at_plot = ax_list[2].plot([x[p] for x in action_tendencies],label=UnitModel.get_list_names(model.actions)[p],linewidth=2)

        ax_list[0].legend(loc=3)
        ax_list[1].legend(loc=3)
        ax_list[2].legend(loc=3)
        # for p in range(0, len(states_values[0])):
        #
        #     elicitors_plot = ax_list[2].plot(
        #         y_vals,
        #         [e[p] for e in scale(elicitor_values, 10, y_pos_elicitor)],
        #         color=my_cols[p])
        #     at_plot = ax_list[3].plot(y_vals, [a[p] for a in scale(action_tendencies, 20, y_pos_action_ten)],
        #                               color=my_cols[p])

        fontP = FontProperties()
        fontP.set_size('small')

        ax_actions = ax_list[3]
        action_colormap = mpl.colors.ListedColormap(["#999999"]+my_cols[0:(set(action_values_i).__len__()-1)]) #mpl.colors.ListedColormap(plt.rcParams['axes.prop_cycle'].by_key()['color'])
        ax_actions.imshow([action_values_i, action_values_i, action_values_i], interpolation='none',cmap=action_colormap)


        print("SHOWING PLOT; WAITING FOR PLOT TO BE CLOSED BEFORE CONTINUING.")
        plt.show(block=True)
        return plt
