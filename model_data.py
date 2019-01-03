import numpy as np
#from minimal_example_interface import *

def multiplicative_term(kappa_val, r_array, cue_array):
    assert (type(kappa_val) == float or type(kappa_val) == int)
    assert (type(r_array) == np.ndarray)
    assert (type(cue_array) == np.ndarray)

    return ({"kappa": kappa_val, "r": r_array, "cue": cue_array})

def SaltSugarModelWithCue_SingleTerm(term):
    return term['kappa']*term['r']*term['cue']

def SaltSugarModelWithCue(term_list):
    return sum([SaltSugarModelWithCue_SingleTerm(term) for term in term_list])

cue=np.array([1.0,1.0,0.0])
term_Na=multiplicative_term(1.5,np.array([1.0,1.0,0.0]),cue)
term_h=multiplicative_term(1,np.array([0.0,-1.0,0.0]),cue)
term_Glc=multiplicative_term(1,np.array([0.0,0.0,1.0]),cue)

#so in this particular experiment, cue doesn't vary.
#what we want to show is the result we get when we plug in the values
#so we might want to solve for something here...

#let's use aggregate numbers
from get_data import *
data_exp_1.columns
data_exp_1.groupby(['DepletionDescription','ConcentrationAmount']).mean().loc[:,'Lick number']

data_exp_1.groupby(['DepletionDescription','ConcentrationAmount']).mean().loc[:,'Latency']