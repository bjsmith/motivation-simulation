import matplotlib.pyplot as plt #we might do some other tool later.
from SimulationVisualization import *
__author__ = 'benjaminsmith'
from SetupBaseSaltRatModel import *
import Tkinter as tk

model = setup_base_salt_rat_model()

base_hz=5

model.states[i_salt].value = 1.0
model.set_display_settings(graph_title="Status: Induced saliene deficiency")
for i in range(0,10):
    model.step()

dpi = 80
fig_height = 8.0
fig_width = 10.0
my_cols = ['r', 'b', '#009900', '#999900', '#990099']

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

ax_list[0].set_title("Actions")
ax_list[1].set_title("States")
ax_list[2].set_title("Elicitors")
ax_list[3].set_title("Action Tendencies")

plt.tight_layout()

for p in range(0, len(states_values[0])):
    states_plot = ax_list[1].plot(y_vals,
                                  [s[p] for s in scale(states_values, 10, y_pos_states)],
                                  label=model.record[0]['states'][p].name
                                  , color=my_cols[p])
    elicitors_plot = ax_list[2].plot(
        y_vals,
        [e[p] for e in scale(elicitor_values, 10, y_pos_elicitor)],
        color=my_cols[p])
    at_plot = ax_list[3].plot(y_vals, [a[p] for a in scale(action_tendencies, 20, y_pos_action_ten)], color=my_cols[p])

fontP = FontProperties()
fontP.set_size('small')

ax_actions=ax_list[0]


ax_actions.imshow([action_values_i,action_values_i,action_values_i],interpolation='none')
ax_main_pos.colormap = mpl.colors.ListedColormap(my_cols)


plt.show(block=True)