#importing widgets
from ipywidgets import widgets
from IPython.display import display

#some helper functions for the latex equation
def ndarray_latex_format(np_ndarray):
    return '\\begin{bmatrix}' + " \\\\ ".join([str(round(x,2)) for x in np_ndarray]) + '\\end{bmatrix}'

def krc_term_to_latex(term):
    return str(term["kappa"]) + " \\times " + ndarray_latex_format(term['r']) +  "\\circ " + ndarray_latex_format(term['cue'])



#set up buttons
bResetAll=widgets.Button(description='Reset to Defaults')
bSatiationPreset=widgets.Button(description='Salt Satiated')
bDeprivationPreset=widgets.Button(description='Salt Deprived')
tbSugarPresence=widgets.ToggleButton(value=False, description='Sugar present')

#set up input boxes
header_labels = ['Na','hydration','Glucose']
row_labels = ['Moderate Salt','Strong Salt', 'Sugar']

ftKappaVals = [widgets.FloatText(value=0, description=drive) for drive in header_labels]


ftRewardVals = [widgets.VBox([widgets.Label(rl) for rl in (['Solution'] + row_labels)])] + [
     widgets.VBox([widgets.Label(j)] + [widgets.FloatText(value=0,layout=widgets.Layout(width='100px')) for i in range(0,3) ])
     for j in header_labels
    ]

ftCueVals = [widgets.FloatText(value=0,description = sln) for sln in row_labels]

full_control_list=ftKappaVals+[sln for driveset in ftRewardVals[1:] for sln in driveset.children[1:]]+ftCueVals
#set up indices for input boxes
i_Na=0
i_h=1
i_Glc=2
i_Moderate_Na_Sln=0
i_Strong_Na_Sln=1
i_Sugar_Sln=2

#set up click events for buttons
def bResetAll_on_click(b):
    """This needs to set all the values for all the textboxes"""
    
    #kappas
    ftKappaVals[i_Na].value = 1.0
    ftKappaVals[i_h].value = 1.0
    ftKappaVals[i_Glc].value = 1.0
    
    #expected rewards
    ftRewardVals[1+i_Na].children[1+i_Moderate_Na_Sln].value = 0.5
    ftRewardVals[1+i_Na].children[1+i_Strong_Na_Sln].value = 1.0
    ftRewardVals[1+i_Na].children[1+i_Sugar_Sln].value = 0
    ftRewardVals[1+i_h].children[1+i_Moderate_Na_Sln].value = 0
    ftRewardVals[1+i_h].children[1+i_Strong_Na_Sln].value = -1.0
    ftRewardVals[1+i_h].children[1+i_Sugar_Sln].value = 0
    ftRewardVals[1+i_Glc].children[1+i_Moderate_Na_Sln].value = 0
    ftRewardVals[1+i_Glc].children[1+i_Strong_Na_Sln].value = 0
    ftRewardVals[1+i_Glc].children[1+i_Sugar_Sln].value = 1
    
    #presence
    ftRewardVals[1+i_Moderate_Na_Sln].value=1
    ftRewardVals[1+i_Strong_Na_Sln].value=1
    ftRewardVals[1+i_Sugar_Sln].value=2

def bDeprivationPreset_on_click(b):
    """Deprivation preset mainly needs to set interoception for Na up high"""
    ftKappaVals[i_Na].value = 1.0
    #but we also want to set the others to sensible values.
    ftKappaVals[i_h].value=1.0
    update_equation()
    
    
def bSatiationPreset_on_click(b):
    """Satiation prseet mainly needs to set interoception for Na down low"""
    ftKappaVals[i_Na].value = -1.0
        #but we also want to set the others to sensible values.
    ftKappaVals[i_h].value=1.0
    
def tbSugarPresence_on_change(change):
    """Sugar toggle set the sugar value to whatever the toggle is."""
    ftCueVals[i_Glc].value = int(change.new)
    #I don't like the default styling
    if(change.new==False): tbSugarPresence.icon=''
    if(change.new): tbSugarPresence.icon='check'
        
def update_equation():
    value_C=np.array([ftRewardVals[1+i].value for i in range(0,3)])
    term_Na=multiplicative_term(ftKappaVals[i_Na].value,
                                np.array([ftRewardVals[1+i_Na].children[1+i].value for i in range(0,3)]),
                                value_C
                                )
    term_h=multiplicative_term(ftKappaVals[i_h].value,
                                np.array([ftRewardVals[1+i_h].children[1+i].value for i in range(0,3)]),
                                value_C
                                )
    term_Glc=multiplicative_term(ftKappaVals[i_Glc].value,
                                np.array([ftRewardVals[1+i_Glc].children[1+i].value for i in range(0,3)]),
                                value_C
                                )

#wire up buttons to their event handlers
bDeprivationPreset.on_click(bDeprivationPreset_on_click)
bSatiationPreset.on_click(bSatiationPreset_on_click)
bResetAll.on_click(bResetAll_on_click)
tbSugarPresence.observe(tbSugarPresence_on_change, names='value')

#reset all to start.
bResetAll_on_click(bResetAll)