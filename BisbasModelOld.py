import numpy as np
import matplotlib.pyplot as plt #we might do some other tool later.
from ActionModel import ActionModel
from StandardLayer import *
import collections
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
                 action_tendency_persistence
                 ):
        assert learning_rate<1
        assert action_tendency_persistence<1

        self.learning_rate=learning_rate

        #let's take states, actions, and elicitors each as either lists, dictionaries, or numbers. But we store them as an ordered dictionary


        self.action_tendency_persistence=action_tendency_persistence

        self.states = getStandardLayer(states,"State")
        self.actions = [ActionModel("Action" + str(i),0,0,baseline_pos_expectancy,baseline_neg_expectancy,1,1,baseline_action_threshold,0)
                        for i in (range(1,action_state_elicitations+1))]

        self.environment_elicitations = getStandardLayer(elicitors,"Elicitor")
            #which expectancies the environment elicits at any moment
        #may want to extend this by for instance, adding a constant "exploration" that determines how much this
        #model weights positive over negative expectancies.
        #this may be unnecessary though.
        self.consummatory_power = np.diag((len(self.actions),len(self.states)))
        self.fig=None
        self.axes_list=None
            #consummatory power of each action on each state

    #http://stackoverflow.com/questions/141545/overloading-init-in-python
    @classmethod
    def asSimpleModel(cls,
                      action_state_elicitations,
                 baseline_pos_expectancy,
                 baseline_neg_expectancy,
                 baseline_action_threshold,
                 learning_rate,
                 action_tendency_persistence):
        assert learning_rate<1
        assert action_tendency_persistence<1

        self.learning_rate=learning_rate
        self.action_tendency_persistence=action_tendency_persistence
        self.states = [0.0]*action_state_elicitations
        self.actions = [ActionModel("Action" + str(i),0,0,baseline_pos_expectancy,baseline_neg_expectancy,1,1,baseline_action_threshold,0)
                        for i in (range(1,action_state_elicitations+1))]

        self.environment_elicitations = [0.0]*action_state_elicitations
            #which expectancies the environment elicits at any moment
        #may want to extend this by for instance, adding a constant "exploration" that determines how much this
        #model weights positive over negative expectancies.
        #this may be unnecessary though.
        self.consummatory_power = np.diag((len(self.actions),len(self.states)))
        self.fig=None
        self.axes_list=None
            #consummatory power of each action on each state
        return(cls.)
    def step(self):
        #
        #step through one full iteration of the model
        #calculate action tendencies for new round.
        #a fancier implementation should probably automatically copy the current state and then calculate everything
        #in next state from current state
        #this will do for now
        for i,action in enumerate(self.actions):
            assert isinstance(action, ActionModel)
            #set the action tendency for the next timepoint
            action.tendency=(action.pos_expectancy*self.states[i]*self.environment_elicitations[i]
                             - action.neg_expectancy*self.states[i]*self.environment_elicitations[i]
                             +action.tendency*self.action_tendency_persistence)
                #for now, we haven't implemented a "fun-seeking" parameter which would build the model toward
                #optimizing the greatest reward regardless of possible pain. Partly because it seems like we ought to
                #have a corresponding "pain-avoidance" parameter, but I don't have theoretical justification for it.
                #also - would be nice to see if we can get it to emerge naturally somehow.
            #*then* set the action
            #reset action value
            self.actions[i].value=0

        #self.display_current_state_text()
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
        for i,action in enumerate(self.actions):
            for j,state in enumerate(self.states):
                self.states[j]-=self.consummatory_power[i,j]*self.actions[i].value

        # learning model
        #expected reward = expected reward_{t-1}*(1-learning_rate)+actual_reward*(l)
        max_tendency_action.pos_expectancy = (
            max_tendency_action.pos_expectancy*(1-self.learning_rate) +
            max_tendency_action.pos_val*(self.learning_rate))
        print("learning rate:")
        print(self.learning_rate)
        print(max_tendency_action.pos_expectancy)
        print(max_tendency_action.pos_val)
        #expected punishment = expected punishment_{t-1)*(1-learning_rate)+actual-reward*l
        max_tendency_action.neg_expectancy = (
            max_tendency_action.neg_expectancy*(1-self.learning_rate) +
            max_tendency_action.neg_val*(self.learning_rate))
        #self.display_current_state_text()

    def current_action(self):
        cur_action_str = ""
        for action in self.actions:
            if(action.value<>0):
                cur_action_str = cur_action_str + action.name + "(" + str(action.value)+")"
        return cur_action_str


    def display_current_state_text(self):
        #should present:
        #Constant parameters
        #print_new_line("Model constants",weight='bold')
        print("MODEL CONSTANTS")
        print("Learning rate: " + str(self.learning_rate))
        print("Action Tendency Persistence: " + str(self.action_tendency_persistence))
        print("Consummatory power")
        print(str(self.consummatory_power))
        for action in self.actions:
            print action
        #print_new_line("Expectancies: Pos=" + str(bb.))

        #Current state (organism)
        print("CURRENT STATE")
        print("States:" + str(self.states))
        print("Environment elicitations:" + str(self.environment_elicitations))
        print("Current action(s):")
        for action in self.actions:
            if(action.value<>0):
                print action.name + "(" + str(action.value)+")"

        #current state (environment)
        print("CURRENT ENVIRONMENT STATE")


    def display_current_state(self):
        assert isinstance(self,BisbasModel)
        #http://matplotlib.org/api/pyplot_api.html
        #these should really only be defined anew here if a figure doesn't already exist.
        vert_axes=3
        horiz_axes=2
        dpi=80

        if(self.fig is None):
            fig_height=8.0#figure height in inches
            fig_width=12.0#figure width in inches
            fig, axes_list = plt.subplots(vert_axes,horiz_axes,dpi=dpi,figsize=(fig_width,fig_height))  # a figure with a 2x2 grid of Axes
            self.fig = fig
            self.axes_list = axes_list
        else:
            fig = self.fig
            fig_height=fig.get_figheight()
            fig_width=fig.get_figwidth()
            axes_list = self.axes_list
            #fig.clf()
            for ax in axes_list.flatten():
                ax.cla()

        #OK so it's four inches tall. That means that if we use a 12pt font we have 72*4/12=24 line plot.
        line_height=16.0/72/fig_height*vert_axes#as a fraction of the whole thing.
        left_margin=12.0*2/72/fig_width*horiz_axes
        ax_cur_action = axes_list[0,0]
        ax_cur_action.set_axis_off()
        #get current action
        ax_cur_action.text(0,1,"Current Action:",weight='bold',fontsize=16)
        ax_cur_action.text(0,1-line_height,self.current_action(),weight='bold',fontsize=16)
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
        for i, ee in enumerate(self.environment_elicitations):
            if (ee>0):
                ee_text = action_names[i] + " (" +str(ee)+")"
                ax_environment.text(0,1-line_height*(i+1),ee_text)

        #draw state graph

        ax_state=axes_list[1,1]
        assert isinstance(ax_state,plt.Axes)
        ypos=np.arange(len(self.states))
        plt_tendency=ax_state.barh(ypos, self.states,align='center')
        ax_state.set_yticks(ypos)
        ax_state.set_yticklabels(action_names)
        ax_state.set_title("Internal State")


        #Learned values readout
        ax_learned_values=axes_list[2,1]
        ax_learned_values.set_title("Learned values:")
        ax_learned_values.set_axis_off()
        p_name=0
        col_incr=(1-.5)/4
        p_pe=0.5
        p_ne=0.5+col_incr*1
        p_pv=0.5+col_incr*2
        p_nv=0.5+col_incr*3
        ax_learned_values.text(p_name,0.8,a.name,fontsize=12)
        ax_learned_values.text(p_pe,0.8,"+Exp",fontsize=12)
        ax_learned_values.text(p_ne,0.8,"-Exp",fontsize=12)
        ax_learned_values.text(p_pv,0.8,"+Val",fontsize=12)
        ax_learned_values.text(p_nv,0.8,"-Val",fontsize=12)

        for i, a in enumerate(self.actions):
            ax_learned_values.text(p_name,0.8-line_height*(i+1),a.name,fontsize=12)
            ax_learned_values.text(p_pe,0.8-line_height*(i+1),"{0:0.1f}".format(a.pos_expectancy),fontsize=12)
            ax_learned_values.text(p_ne,0.8-line_height*(i+1),"{0:0.1f}".format(a.neg_expectancy),fontsize=12)
            ax_learned_values.text(p_pv,0.8-line_height*(i+1),"{0:0.1f}".format(a.pos_val),fontsize=12)
            ax_learned_values.text(p_nv,0.8-line_height*(i+1),"{0:0.1f}".format(a.neg_val),fontsize=12)

        #and we don't need the remaining graph.
        axes_list[2,0].set_axis_off()










