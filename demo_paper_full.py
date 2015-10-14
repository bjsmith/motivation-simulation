import matplotlib.pyplot as plt #we might do some other tool later.
__author__ = 'benjaminsmith'
from SetupBaseStudentModel import *

#first model showing within-subject changes.
bb = setup_base_student_model()
bb.display_current_state()

bb.elicitors[i_friends].value=1
bb.elicitors[i_study].value =1
#second models showing between-subject differences.

while bb.actions[i_study]==0:
    bb.step()
    bb.
bb.display_current_state()
plt.pause(5)


