from UnitModel import *
__author__ = 'benjaminsmith'

"""Inherits from UnitModel"""
class ActionROModel(UnitModel):
    """Set initial ActionModel."""
    def __init__(self,action_name,tendency,value,pos_expectancy,neg_expectancy,threshold,chaos,persistence):
        super(ActionROModel,self).__init__(action_name,value)
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
        self.chaos=chaos

    def __repr__(self): #let's not do this for now.
    #def __print__(self):

        return ("ActionROModel " + self.name + "(ten=" +
               str(self.tendency) + ",value=" + str(self.value) +
        ",pe=" + str(self.pos_expectancy) +
        ",ne=" + str(self.neg_expectancy) +
        ") ")# + super(ActionModel,self).__repr__(self))


