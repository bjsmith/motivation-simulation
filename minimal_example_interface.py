#importing widgets
import numpy as np
from ipywidgets import widgets
from IPython.display import display
from IPython.display import Markdown


#some helper functions for the latex equation
def ndarray_latex_format(np_ndarray,rounding=2):
    return '\\begin{bmatrix}' + " \\\\ ".join([str(round(x,rounding)) for x in np_ndarray]) + '\\end{bmatrix}'

def krc_term_to_latex(term,rounding=2):
    return str(term["kappa"]) + " \\times " + ndarray_latex_format(term['r'],rounding) +  "\\circ " + ndarray_latex_format(term['cue'])



#set up buttons
bResetAll=widgets.Button(description='Reset to Defaults')
bSatiationPreset=widgets.Button(description='Salt Satiated')
bDeprivationPreset=widgets.Button(description='Salt Deprived')
bRecalculate=widgets.Button(description='Recalculate')
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

#set up the equation and wire up its calculation functions

#have to define these via function calls because we wnat the main definitions
#defined on the main page but want to use them here. To use them here they have 
#to be passed in as functions.
SingleTerm_Calculation_Function=None
def set_singleterm_calculation_function(SaltSugarModelWithCue_SingleTerm):
    global SingleTerm_Calculation_Function
    SingleTerm_Calculation_Function = SaltSugarModelWithCue_SingleTerm
    
Model_Calculation_Function=None
def set_model_calculation_function(SaltSugarModelWithCue):
    global Model_Calculation_Function
    Model_Calculation_Function = SaltSugarModelWithCue
    
equation_markdown_text_unformatted="""
$$
\\begin{{align}}
\\begin{{split}}
\\tilde r(\mathbf{{r}},\mathbf{{\kappa}},\mathbf{{c}})= & 
\kappa_{{\\text{{Na}}}} \mathbf{{r}}_{{\\text{{Na}}}}\mathbf{{c}} 
& + \kappa_{{h}} \mathbf{{r}}_{{h}}\mathbf{{c}}
& + \kappa_{{\\text{{Glc}}}} \mathbf{{r}}_{{\\text{{Glc}}}}\mathbf{{c}} \\\\
 = & {Na_term} & + {h_term} & + {Glc_term} \\\\
 = & {Na_val} & + {h_val} & + {Glc_val} \\\\
 = & {function_val} \\begin{{matrix}} \\textit{{{sln1_val}}}\\\\ \\textit{{{sln2_val}}}\\\\ \\textit{{{sln3_val}}} \\end{{matrix}}
\end{{split}}
\end{{align}}
$$
"""

def get_and_format_main_equation_text(term_Na,term_h,term_Glc,three_solutions=['Moderate Salt solution','Strong salt solution','Sugar solution']):
    return equation_markdown_text_unformatted.format(Na_term=krc_term_to_latex(term_Na), 
        h_term=krc_term_to_latex(term_h,rounding=4),
        Glc_term=krc_term_to_latex(term_Glc),
        Na_val=ndarray_latex_format(SingleTerm_Calculation_Function(term_Na)),
        h_val=ndarray_latex_format(SingleTerm_Calculation_Function(term_h),rounding=4),
        Glc_val=ndarray_latex_format(SingleTerm_Calculation_Function(term_Glc)),
                                                     sln1_val = three_solutions[0],
                                                     sln2_val=three_solutions[1],
                                                     sln3_val=three_solutions[2],
        function_val=ndarray_latex_format(Model_Calculation_Function([term_Na,term_h,term_Glc])))


#function to update the equation terms.
def get_updated_equation_terms(term_function):
    """returns the new terms to be used in the equation"""
    value_C=np.array([ftCueVals[i].value for i in range(0,3)])
    term_Na=term_function(ftKappaVals[i_Na].value,
                                np.array([ftRewardVals[1+i_Na].children[1+i].value for i in range(0,3)]),
                                value_C
                                )
    term_h=term_function(ftKappaVals[i_h].value,
                                np.array([ftRewardVals[1+i_h].children[1+i].value for i in range(0,3)]),
                                value_C
                                )
    term_Glc=term_function(ftKappaVals[i_Glc].value,
                                np.array([ftRewardVals[1+i_Glc].children[1+i].value for i in range(0,3)]),
                                value_C
                                )
    return {"Na":term_Na,"h":term_h,"Glc":term_Glc}

term_function=None
def set_term_function(new_term_function):
    global term_function
    term_function=new_term_function
    
def update_equation():
    new_terms=get_updated_equation_terms(term_function)
    math_widget.value = get_and_format_main_equation_text(new_terms['Na'],new_terms['h'],new_terms['Glc'])

#set up equation
math_widget=widgets.HTMLMath(value='$$')

#set up click events for buttons
def bResetAll_on_click(b):
    """This needs to set all the values for all the textboxes"""
    
    #kappas
    ftKappaVals[i_Na].value = 1.5
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
    ftCueVals[i_Moderate_Na_Sln].value=1
    ftCueVals[i_Strong_Na_Sln].value=1
    ftCueVals[i_Sugar_Sln].value=0

def bDeprivationPreset_on_click(b):
    """Deprivation preset mainly needs to set interoception for Na up high"""
    ftKappaVals[i_Na].value = 1.5
    #but we also want to set the others to sensible values.
    ftKappaVals[i_h].value=1.0
    update_equation()
    
    
def bSatiationPreset_on_click(b):
    """Satiation prseet mainly needs to set interoception for Na down low"""
    ftKappaVals[i_Na].value = -1.5
        #but we also want to set the others to sensible values.
    ftKappaVals[i_h].value=1.0
    update_equation()
    
def tbSugarPresence_on_change(change):
    """Sugar toggle set the sugar value to whatever the toggle is."""
    ftCueVals[i_Glc].value = int(change.new)
    #I don't like the default styling
    if(change.new==False): tbSugarPresence.icon=''
    if(change.new): tbSugarPresence.icon='check'
    update_equation()
        


def bRecalculate_on_click(b):
    update_equation()




#wire up buttons to their event handlers
bDeprivationPreset.on_click(bDeprivationPreset_on_click)
bSatiationPreset.on_click(bSatiationPreset_on_click)
tbSugarPresence.observe(tbSugarPresence_on_change, names='value')
bResetAll.on_click(bResetAll_on_click)
bRecalculate.on_click(bRecalculate_on_click)




#reset all to start.
bResetAll_on_click(bResetAll)

def display_main_widget():
    """display the big widget on the main page"""
    
    box_bordered=widgets.Layout(border='solid 1pt black')
#     def widget_header(value):
#         return widgets.Label(value='### ' + value)
    
    reward_box=widgets.VBox([widgets.Label(value='Expected reward ($ \\tilde r$)'),
                                    widgets.HBox(ftRewardVals)],layout=box_bordered)
    cue_box=widgets.VBox([widgets.Label('Cue Accessibility ($\mathbf{c}$)')]+ftCueVals, layout=box_bordered)
    display(widgets.VBox([
        widgets.HBox([bDeprivationPreset,bSatiationPreset,tbSugarPresence,bResetAll]),
        widgets.VBox([widgets.Label('Interoception ($\kappa$)'),
                     widgets.HBox(ftKappaVals)],layout=box_bordered),
        widgets.HBox([reward_box,cue_box]),
        bRecalculate,
        math_widget]))
#old code

#get all the controls in the widget
#full_control_list=ftKappaVals+[sln for driveset in ftRewardVals[1:] for sln in driveset.children[1:]]+ftCueVals

#need to convert it into a bloody dictionary.
#equation_out = widgets.interactive_output(f7, full_control_list.to)


