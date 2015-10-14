import matplotlib.pyplot as plt #we might do some other tool later.
__author__ = 'benjaminsmith'
from SetupBaseStudentModel import *

#first model showing within-subject changes.
bb = setup_base_student_model()


bb.display_current_state()

while bb.actions[0].value==0:
    bb.step_and_display(1,2)
    #OK. In order to do copy we're going to have to copy the individual attributes. Otherwise we're currently capturing graph objects and things and that's causing problems.

print("tendency increasing over time:")
print([iter["actions"][0].tendency for iter in bb.record])

bb.step_and_display()

#OK. Now, we introduce a potential partner, friends, and also a study environment
bb.elicitors[i_friends].value=1
bb.elicitors[i_partner].value =1
bb.elicitors[i_study].value =1

bb.step_and_display()

#next task:

#next time model approaches we're in for a shock.
bb.actions[i_partner].neg_val=4
bb.display_current_state()

while bb.actions[2].value==0:
    bb.step()
    bb.display_current_state()
    plt.pause(0.5)
bb.step_and_display(2,0.5)

#it doesn't matter that next time there's no negative...damage is done!
for i in range(0,5):
    bb.actions[2].neg_val=0
    bb.step()
    bb.display_current_state()
    plt.pause(0.5)

#take away other options, finally study happens.
for e in bb.elicitors:
    if e.name=="Food":
        e.value=0.0
    elif e.name=="Friends":
        e.value=0.0
    elif e.name=="Potential partner":
        e.value=0.0
for s in bb.states:
    if e.name=="SocialNeed":
        e.value=1.0
bb.step_and_display(15,5)

bb.elicitors[i_fear_threat].value=1.0
bb.states[i_fear_threat].value=1.0

bb.step_and_display(15,5)

#OK. Let's say the individual is hungry again.
bb.states[i_food].value=1.0
bb.elicitors[i_food].value=1.0
bb.step_and_display(20,5)
