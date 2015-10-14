from UnitModel import *
__author__ = 'benjaminsmith'

"""Inherits from UnitModel"""
class ActionModel(UnitModel):
    """Set initial ActionModel."""
    def __init__(self,action_name,tendency,value,pos_expectancy,neg_expectancy,pos_val,neg_val,threshold,chaos,persistence):
        super(ActionModel,self).__init__(action_name,value)
        #user interface
        #self.name = str(action_name)

        #psychology
        self.tendency=tendency
        self.persistence = persistence
        #self.value = value
        self.pos_expectancy=pos_expectancy
        self.neg_expectancy=neg_expectancy
        self.threshold=threshold

        #environment
        self.pos_val=pos_val
        self.neg_val=neg_val
        self.chaos=chaos

    def __repr__(self): #let's not do this for now.
    #def __print__(self):

        return ("ActionModel " + self.name + "(ten=" +
               str(self.tendency) + ",value=" + str(self.value) +
        ",pe=" + str(self.pos_expectancy) +
        ",ne=" + str(self.neg_expectancy) +
        ",pv=" + str(self.pos_val) +
        ",nv=" + str(self.neg_val) +
        ") ")# + super(ActionModel,self).__repr__(self))