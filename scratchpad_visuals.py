import numpy as np
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
               baseline_action_threshold=4,
               learning_rate=0.1,
               action_tendency_persistence=0.9)


#http://matplotlib.org/api/pyplot_api.html
fig_height=4#figure height in inches
fig_width=8#figure width in inches
dpi=80
fig, ax_lst = plt.subplots(1,2,dpi=dpi,figsize=(8,fig_height))  # a figure with a 2x2 grid of Axes

#OK so it's four inches tall. That means that if we use a 12pt font we have 72*4/12=24 line plot.
line_height=14.0/72/fig_height#as a fraction of the whole thing.
left_margin=12.0*2/72/fig_width
    #this doesn't really work...probably because the axis is well less than half of the space itself
#let's leave a littel space between lines
#let's stick with some object oriented shit

axs_left = ax_lst[0]
axs_left.set_axis_off()


my_color= (51./255., 51./255., 51./255.)


axs_left.set_title("Bisbas Model Information",
                        color=my_color, fontsize=14, weight='bold')

def print_new_line(text,**kwargs):
    axs_left.text(left_margin,1-line_height*print_new_line.iter_line,text,fontsize=12,**kwargs)
    print_new_line.iter_line +=1

print_new_line.iter_line=1


#should present:
#Constant parameters
#print_new_line("Model constants",weight='bold')
print_new_line("Model constants")
print_new_line("Learning rate: " + str(bb.learning_rate))
print_new_line("Consummatory power" + str(bb.consummatory_power))
#print_new_line("Expectancies: Pos=" + str(bb.))

#Current state (organism)
print_new_line("States:" + str(bb.states))
print_new_line("Environment elicitations:" + str(bb.environment_elicitations))

#current state (environment)

def print_current_state(bb_model,fig,ax_lst):

    assert isinstance(bb_model,BisbasModel)
    #http://matplotlib.org/api/pyplot_api.html
    vert_axes=3
    horiz_axes=2
    dpi=80

    if(fig!=None):
        fig_height=fig.get_figheight()
        fig_width=fig.get_figwidth()
    else:
        fig_height=8#figure height in inches
        fig_width=8#figure width in inches
        fig, ax_lst = plt.subplots(vert_axes,horiz_axes,dpi=dpi,figsize=(fig_width,fig_height))  # a figure with a 2x2 grid of Axes
    #OK so it's four inches tall. That means that if we use a 12pt font we have 72*4/12=24 line plot.
    line_height=16.0/72/fig_height*vert_axes#as a fraction of the whole thing.
    left_margin=12.0*2/72/fig_width*horiz_axes
    ax_cur_action = ax_lst[0,0]
    ax_cur_action.set_axis_off()
    #get current action
    ax_cur_action.text(0,1,"Current Action:",weight='bold')
    ax_cur_action.text(0,1-line_height,bb_model.current_action(),weight='bold')
    action_names = [a.name for a in bb_model.actions]
    #action_vals = [a.value for a in bb_model.actions]

    #draw action tendency graph
    action_tendency = [a.tendency for a in bb_model.actions]
    action_threshold = [a.threshold for a in bb_model.actions]
    ax_tendency=ax_lst[0,1]
    assert isinstance(ax_tendency,plt.Axes)
    ypos=np.arange(len(action_tendency))
    plt_tendency=ax_tendency.barh(ypos, action_tendency,align='center')
    ax_tendency.set_yticks(ypos)
    ax_tendency.set_yticklabels(action_names)
    ax_tendency.set_title("Action Tendency")

    for i, th in enumerate(action_threshold):
        print(i)
        ax_tendency.plot([th,th],[i-0.4,i+0.4],color="#ff0000")

    #draw environment graph
    ax_environment = ax_lst[1,0]
    ax_environment.set_title("Environment Facilitates:")
    ax_environment.set_axis_off()
    for i, ee in enumerate(bb_model.environment_elicitations):
        if (ee>0):
            ee_text = action_names[i] + " (" +str(ee)+")"
            ax_environment.text(0,1-line_height*(i+1),ee_text)

    #draw state graph

    ax_state=ax_lst[1,1]
    assert isinstance(ax_state,plt.Axes)
    ypos=np.arange(len(bb_model.states))
    plt_tendency=ax_state.barh(ypos, bb_model.states,align='center')
    ax_state.set_yticks(ypos)
    ax_state.set_yticklabels(action_names)
    ax_state.set_title("Internal State")


    #Learned values readout
    ax_learned_values=ax_lst[2,1]
    ax_learned_values.set_title("Learned values:")
    ax_learned_values.set_axis_off()
    p_name=0
    col_incr=(1-.5)/4
    p_pe=0.5
    p_ne=0.5+col_incr*1
    p_pv=0.5+col_incr*2
    p_nv=0.5+col_incr*3
    ax_learned_values.text(p_name,0.8,a.name,fontsize=10)
    ax_learned_values.text(p_pe,0.8,"+Exp",fontsize=10)
    ax_learned_values.text(p_ne,0.8,"-Exp",fontsize=10)
    ax_learned_values.text(p_pv,0.8,"+Val",fontsize=10)
    ax_learned_values.text(p_nv,0.8,"-Val",fontsize=10)

    for i, a in enumerate(bb_model.actions):
        ax_learned_values.text(p_name,0.8-line_height*(i+1),a.name,fontsize=10)
        ax_learned_values.text(p_pe,0.8-line_height*(i+1),str(a.pos_expectancy),fontsize=10)
        ax_learned_values.text(p_ne,0.8-line_height*(i+1),str(a.neg_expectancy),fontsize=10)
        ax_learned_values.text(p_pv,0.8-line_height*(i+1),str(a.pos_val),fontsize=10)
        ax_learned_values.text(p_nv,0.8-line_height*(i+1),str(a.neg_val),fontsize=10)

    #and we don't need the remaining graph.
    ax_lst[2,0].set_axis_off()