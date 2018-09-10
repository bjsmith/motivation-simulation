import numpy as np
import sys
import matplotlib.pyplot as plt #we might do some other tool later.
from copy import *
from ActionModel import ActionModel
from ActionROModel import ActionROModel
from UnitModel import UnitModel
import textwrap
from scipy.stats import norm
import collections
import time
#see Python GUI (http://www.cosc.canterbury.ac.nz/greg.ewing/python_gui/)
#and http://insights.dice.com/2014/11/26/5-top-python-guis-for-2015/


class BisbasModel:
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
        assert learning_rate<1
        assert action_tendency_persistence<1
        assert satiation_power<1
        assert consummatory_power<1

        self.graph_width=None
        self.graph_title_text = None

        self.learning_rate = learning_rate
        self.gains_v_losses = gains_v_losses

        if action_tendency_function is None:
            self.action_tendency_function=lambda x:x
        else:
            self.action_tendency_function=action_tendency_function

        #let's take states, actions, and elicitors each as either lists, dictionaries, or numbers.
        # But we store them as an ordered dictionary
        #self.action_tendency_persistence=action_tendency_persistence

        self.states = UnitModel.GetLayerOfUnits(states,"State")
        self.actions = [ActionModel(a.name,
                                    0,
                                    a.value,
                                    baseline_pos_expectancy,baseline_neg_expectancy,1,1,
                                    baseline_action_threshold,
                                    0,
                                    action_tendency_persistence)
                        for a in actions]

        self.elicitors = UnitModel.GetLayerOfUnits(elicitors,"Elicitor")
        #which expectancies the environment elicits at any moment
        #may want to extend this by for instance, adding a constant "exploration" that determines how much this
        #model weights positive over negative expectancies.
        #this may be unnecessary though.

        #graphics
        self.fig=None
        self.axes_list=None
            #consummatory power of each action on each state

        #now we need to record the interactions between each layer:

        def get_layer_interaction(l1, l2):
            if len(l1)==len(l2):
               return np.diag([1.0]*len(l1))
            else: return np.zeros((len(l1),len(l2)))

        #1) Elicitor->ActionTendency
        #if n(state)=n(actions) then we use np.diag as a default
        self.elicitor_action= get_layer_interaction(self.elicitors,self.actions)

        #otherwise, we use np.zeros
        #2) State->ActionTendency
        self.state_action = get_layer_interaction(self.states,self.actions)

        #3) Action->State (SatiationPower)
        self.action_state = get_layer_interaction(self.actions,self.states) * satiation_power

        #4) Action->Elicitor (ConsummatoryPower)
        self.action_elicitor = get_layer_interaction(self.actions,self.elicitors) * consummatory_power

        #5) Elicitor->State ()
        self.elicitor_state = get_layer_interaction(self.elicitors,self.states) * 0 #default is no connection directly from elicitors to state

        #cool
        self.record= []
        #to be a record for previous states.
        self.record_current_values() #record starting values.

    def set_display_settings(self,graph_width=None,tendency_graph_width=None,state_graph_width=None,graph_title=None):
        if(graph_width is not None):
            self.tendency_graph_width = tendency_graph_width
            self.state_graph_width = state_graph_width
        if(tendency_graph_width is not None):
            self.tendency_graph_width = tendency_graph_width
        if state_graph_width is not None:
            self.state_graph_width=state_graph_width
        if(graph_title is not None):
            self.graph_title_text=graph_title



    #http://stackoverflow.com/questions/141545/overloading-init-in-python
    @classmethod
    def asSimpleModel(cls,
                      action_state_elicitations,
                 baseline_pos_expectancy,
                 baseline_neg_expectancy,
                 baseline_action_threshold,
                 learning_rate,
                 action_tendency_persistence):

        return(cls(action_state_elicitations,UnitModel.GetLayerOfUnits(action_state_elicitations),action_state_elicitations,
                   baseline_pos_expectancy,
                   baseline_neg_expectancy,
                   baseline_action_threshold,
                   learning_rate,
                   action_tendency_persistence))

    """n describes the number of times to step
    hz describes the number of operations per second"""
    def step_and_display(self,n=1,hz=1,write_to_file=False):
        for i in range(0,n):
            self.step()
            print("hz="+str(hz))
            delay = 1.0/hz
            print(delay)
            print("size="+str(sys.getsizeof(self.record)))
            #print(time.time())
            plt.pause(delay)
            #print(time.time())
            self.display_current_state()


    def step_repeatedly(self,n=1,silent=True):
        for i in range(0,n):
            self.step(silent=silent)

    def step(self,bb_record=[],silent=True):
        #this function steps one instant through running the model.
        #we need to figure out a good way to record progress of the model over time!

        print([a.value for a in self.actions])
        #calculate action tendency for the next timepoint
        print("used for action tendency:")
        print(self.actions)
        print(self.states)
        print(self.elicitors)

        action_tendency_this = (
            self.action_tendency_function(
                np.array([a.pos_expectancy for a in self.actions]) *
                np.dot([u.value for u in self.states],self.state_action) *
                np.dot([u.value for u in self.elicitors],self.elicitor_action)
            ) -
            self.action_tendency_function(
                np.array([a.neg_expectancy for a in self.actions]) *
                np.dot([u.value for u in self.states],self.state_action) *
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
            assert isinstance(action, ActionModel)
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

        #now, the state response to the action
        state_change = np.dot([a.value for a in self.actions],self.action_state)

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
                a.pos_expectancy = (
                    a.pos_expectancy*(1-self.learning_rate) +
                    a.pos_val*(self.learning_rate))
                print("learning rate:")
                print(self.learning_rate)
                print(a.pos_expectancy)
                print(a.pos_val)
                #expected punishment = expected punishment_{t-1)*(1-learning_rate)+actual-reward*l
                #this would apply...if the reinforced value was negative, somehow.
                a.neg_expectancy = (
                    a.neg_expectancy*(1-self.learning_rate) +
                    a.neg_val*(self.learning_rate))
                #self.display_current_state_text()

        #an array was passed recording past values of bisBas model
        #add the current BisbasModel to it.
        #we can't *store* this in the Model itself because it would create recursive copies,
        #since we're using deep recursion. Will probably eventually need to code a kind of ModelSupervisor to handle
        #this kind of thing.

        #record the current state.
        self.record_current_values()

    def record_current_values(self):
        value_record_t_current={"states":deepcopy(self.states),
                                "elicitors":deepcopy(self.elicitors),
                                "actions":deepcopy(self.actions)}
        self.record.append(value_record_t_current)


    def current_action(self):
        cur_action_str = ""
        for action in self.actions:
            if(action.value!=0):
                cur_action_str = cur_action_str + action.name + "(" + str(action.value)+")"
        return cur_action_str


    def display_current_state_text(self):
        #should present:
        #Constant parameters
        #print_new_line("Model constants",weight='bold')
        print("MODEL CONSTANTS")
        print("Learning rate: " + str(self.learning_rate))
        print("Action Tendency Persistence: " + str([a.persistence for a in self.actions]))
        print("Consummatory power")
        print(str(self.action_state))
        for action in self.actions:
            print(action)
        #print_new_line("Expectancies: Pos=" + str(bb.))

        #Current state (organism)
        print("CURRENT STATE")
        print("States:" + str(self.states))
        print("Environment elicitations:" + str(self.elicitors))
        print("Current action(s):")
        for action in self.actions:
            if(action.value!=0):
                print(action.name + "(" + str(action.value)+")")

        #current state (environment)
        print("CURRENT ENVIRONMENT STATE")


    def display_current_state(self,filename_to_write=None):
        assert isinstance(self,BisbasModel)
        #http://matplotlib.org/api/pyplot_api.html
        #these should really only be defined anew here if a figure doesn't already exist.
        vert_axes=3
        horiz_axes=2
        dpi=80

        if(self.fig is None):
            fig_height=8.0#figure height in inches
            fig_width=10.0#figure width in inches
            fig, axes_list = plt.subplots(vert_axes,horiz_axes,dpi=dpi,figsize=(fig_width,fig_height))  # a figure with a 2x23grid of Axes
            self.fig = fig
            self.axes_list = axes_list
            self.fig_title = fig.suptitle("")
        else:
            fig = self.fig
            fig_height=fig.get_figheight()
            fig_width=fig.get_figwidth()
            axes_list = self.axes_list
            #clear each of the axes
            for ax in axes_list.flatten():
                ax.cla()
            #clear the figure.

        if (self.graph_title_text is not None):
            self.fig_title.set_text(self.graph_title_text)
            self.fig_title.set_fontsize(max(18, 18 * 20 / len(self.graph_title_text) * fig_width / 10))

        #OK so it's four inches tall. That means that if we use a 12pt font we have 72*4/12=24 line plot.
        line_height=16.0/72/fig_height*vert_axes#as a fraction of the whole thing.
        #make the font size smaller if the action name is long!
        action_name_fontsize=min(48.0,48*14/(1+len(self.current_action()))*fig_width/16)
        action_nameline_height = action_name_fontsize / 72 / fig_height * vert_axes  # as a fraction of the whole thing.
        left_margin=12.0*2/72/fig_width*horiz_axes
        ax_cur_action = axes_list[0,0]
        ax_cur_action.set_axis_off()
        #get current action
        ax_cur_action.text(0,1,"Current Action:",weight='bold',fontsize=16)
        ax_cur_action.text(0,1-action_nameline_height-line_height,
                           self.current_action(),weight='bold',fontsize=action_name_fontsize)
        action_names = [a.name for a in self.actions]
        #action_vals = [a.value for a in self.actions]

        #draw action tendency graph
        action_tendency = [a.tendency for a in self.actions]
        action_threshold = [a.threshold for a in self.actions]
        ax_tendency=axes_list[0,1]
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
        ax_environment = axes_list[1,0]
        ax_environment.set_title("Environment Facilitates:")
        ax_environment.set_axis_off()
        for i, ee in enumerate(self.elicitors):
            if (ee.value>0):
                ee_text = str(ee)
                ax_environment.text(0,1-line_height*(i+1),ee_text)

        #draw state graph

        ax_state=axes_list[1,1]
        assert isinstance(ax_state,plt.Axes)
        ypos=np.arange(len(UnitModel.get_list_vals(self.states)))
        plt_tendency=ax_state.barh(ypos, UnitModel.get_list_vals(self.states),align='center')
        ax_state.set_yticks(ypos)
        ax_state.set_yticklabels(UnitModel.get_list_names(self.states))

        ax_state.set_title("Internal State")

        if (self.state_graph_width is not None):
            ax_state.set_xlim(-self.state_graph_width / 2.0, self.state_graph_width / 2.0)
            if (self.tendency_graph_width is not None):
                ax_tendency.set_xlim(-self.tendency_graph_width / 2.0, self.tendency_graph_width / 2.0)

        #Learned values readout
        evfs = 9
        ax_learned_values=axes_list[2,1]
        ax_learned_values.set_title("Learned values:")
        ax_learned_values.set_axis_off()
        p_name=0
        col_incr=(1-.5)/4
        p_pe=0.5
        p_ne=0.5+col_incr*1
        p_pv=0.5+col_incr*2
        p_nv=0.5+col_incr*3
        ax_learned_values.text(p_name,0.8,"Value",fontsize=evfs,fontstretch='condensed')
        ax_learned_values.text(p_pe,0.8,"+Exp",fontsize=evfs,fontstretch='condensed')
        ax_learned_values.text(p_ne,0.8,"-Exp",fontsize=evfs,fontstretch='condensed')


        if (isinstance(self.actions[0], ActionModel)):
            ax_learned_values.text(p_pv, 0.8, "+Val", fontsize=evfs, fontstretch='condensed')
            ax_learned_values.text(p_nv, 0.8, "-Val", fontsize=evfs, fontstretch='condensed')
            for i, a in enumerate(self.actions):
                ax_learned_values.text(p_name,0.8-line_height*(i+1),a.name,fontsize=min(evfs,evfs/(len(a.name))*20),fontstretch='condensed')
                ax_learned_values.text(p_pe,0.8-line_height*(i+1),"{0:0.1f}".format(a.pos_expectancy),fontsize=evfs,fontstretch='condensed')
                ax_learned_values.text(p_ne,0.8-line_height*(i+1),"{0:0.1f}".format(a.neg_expectancy),fontsize=evfs,fontstretch='condensed')
                ax_learned_values.text(p_pv,0.8-line_height*(i+1),"{0:0.1f}".format(a.pos_val),fontsize=evfs,fontstretch='condensed')
                ax_learned_values.text(p_nv,0.8-line_height*(i+1),"{0:0.1f}".format(a.neg_val),fontsize=evfs,fontstretch='condensed')
        if(isinstance(self.actions[0],ActionROModel)):
            for i, a in enumerate(self.actions):
                ax_learned_values.text(p_name, 0.8 - line_height * (i + 1), a.name,
                                       fontsize=min(evfs, evfs / (len(a.name)) * 16), fontstretch='condensed')
                ax_learned_values.text(p_pe,0.8-line_height*(i+1),", ".join(["{0:0.1f}".format(x) for x in a.pos_expectancy]),fontsize=evfs,fontstretch='condensed')
                ax_learned_values.text(p_ne,0.8-line_height*(i+1), ", ".join(["{0:0.1f}".format(x) for x in a.neg_expectancy]),fontsize=evfs,fontstretch='condensed')

            # if (isinstance(self.actions,ActionROModel)):
            #     ax_learned_values.text(p_name, 0.8 - line_height * (i + 1), a.name, fontsize=12,
            #                            fontstretch='condensed')
            #     ax_learned_values.text(p_pe, 0.8 - line_height * (i + 1), "{0:0.1f}".format(a.pos_expectancy),
            #                            fontsize=12, fontstretch='condensed')
            #     ax_learned_values.text(p_ne, 0.8 - line_height * (i + 1), "{0:0.1f}".format(a.neg_expectancy),
            #                            fontsize=12, fontstretch='condensed')

        #and we don't need the remaining graph.
        #axes_list[2,0].set_axis_off()

        #yes we do
        axm_fontsize=10
        ax_matrices = axes_list[2,0]
        ax_matrices.set_title("Matrices:")
        ax_matrices.set_axis_off()
        axm_name_x = 0
        axm=0
        col_incr=1.0/(len(self.actions)+1)
        ax_m=0.5
        ax_m=[0.5+col_incr*c for c in range(0,4)]
        ax_n=[0.8-line_height*(i+1) for i in range(0,5)]

        ax0=[0.0,0.8]
        #now we have to print out these matrices. we want to print out all the values:

        ax_matrices.text(ax0[0], ax0[1], "State->Action", fontsize=axm_fontsize, wrap=True,fontweight='bold',fontstretch='condensed')
        #self.elicitor_action= get_layer_interaction(self.elicitors,self.actions)
        #column names
        for a_i, a in enumerate(self.actions):
            ax_matrices.text((a_i+1)*(col_incr), 0.8 - line_height, "\n".join(textwrap.wrap(a.name,14)),
                             fontsize=min(axm_fontsize,axm_fontsize/(len(a.name))*20),wrap=True,fontstretch='condensed')
        #row names
        for s_i, s in enumerate(self.states):
            ax_matrices.text(0, 0.8 - line_height*(s_i+2), s.name, fontsize=min(axm_fontsize,axm_fontsize/(len(s.name))*10),wrap=True,fontstretch='condensed')

        for r_i,r in enumerate(self.state_action):
            for c_i, cell in enumerate(r):
                ax_matrices.text((c_i+1)*(col_incr), 0.8 - line_height * (r_i + 2), "{0:0.1f}".format(cell),
                                       fontsize=axm_fontsize,fontstretch='condensed')

        # state_action
        #2) State->ActionTendency
        #self.state_action = get_layer_interaction(self.states,self.actions)

        #3) Action->State (SatiationPower)
        #self.action_state = get_layer_interaction(self.actions,self.states) * satiation_power

        #4) Action->Elicitor (ConsummatoryPower)
        #self.action_elicitor = get_layer_interaction(self.actions,self.elicitors) * consummatory_power

        #5) Elicitor->State ()
        #self.elicitor_state = get_layer_interaction(self.elicitors,self.states) * 0 #default is no connection directly from elicitors to state












