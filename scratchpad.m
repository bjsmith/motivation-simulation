%vectors represent current cominations of states and traits
%matrices represent mappings of states and traits to action
%but is this mapping the *actual* link to Action?
%or is is it the *learned association* of the states+traits with the
%action? 
%it can't be the *actual* links if we want subjects to learn values of
%states and traits.

%if we say it's the *learned association* of states and traits with
%the action, then we need a mechanism to train those associations
%Learning might happen simultaneously in two steps:
%1) increasing the positive value of an action when it moves the organism
%   towards homeostatis, and 
%2) increasing the negative value of an action when it moves the organism
%   away from homeostatis, and
%3) proportional to the *absolute value* of the reward prediction error (RPE) of
%that turn, (there are options here; could be proportion to the value of
%the reward rather than the RPE), reinforce the association between the state and traits present
%or, proportional to both the RPE, the presence of the states, and the 
%change in homeostasis, reinforce the association between states and traits
%present.
%We're also going to remove the "actual value" thing from the model, as in
%BisBasROModel
%because the actual value will be the sum total of the change in
%homeostasis as a result of the...
%the problem with this is the change in homeostasis will change a lot
%depending on the context. what to do? take away expected value and just
%train the associations based on the instantaneous strength of RPE?

%An additional problem:
%If we simply have one vector representing expectation of present states on actions
% and one representing expectation of present interoception on action
% that means any two states would be interchangeable as long as they both
% lead to the action. Imagine that 
% performing ActionA in EnvironmentA*StateA produces a positive reponse;
% Performing ActionB in EnvironmentB*StateB produces a positive resonse, but
% Performing ActionB in EnvironmentA*StateA produces a *negative* response. 
%Could we learn this properly?
% If we trained on both, then both EnvA and StateA would have a positive
% link to ActionA; we would simply not perform ActionB. No problem.
% So let's say,
% Performing ActionB in EnvironmentA*StateB produces a *negative* response. 
% in this case, EnvironmentA would encourage ActionA while StateB would
% encourage ActionB. There would be conflict and the model would soon learn
% to moderate and avoid ActionB.
%this applies equally as well for Action A in EnvA*StateB; and for Action B
%in EnvA*StateB, and ActionB in EnvB*StateA.

%FIXING AN EXPECTED VALUE TO AN ACTION
%BUT the bigger problem in the current model is that actions have a
%context-invariant expected value. Although this is constrained down to 0
%where the right context isn't available, we can't through this model
%actually *reverse* valence of an action.
%This was done before by creating a negative state...maybe this is OK?
%it's just theoretically very difficult. I think what we want is a
%construct representing predicted end states of an action; "approach" or
%"avoid" are systems that respond to that end-state.
%So I don't know if it's right to have this "expected value" which is a
%fixed positive or negative value to an action. An action in a context 
%has a predicted result; it is this result which is attractive or aversive.
%It might even make sense to build this learning model WITHOUT explicit
%valence, relying only on positive/negative values of homeostasis, and then
%work out how to add in valence later.

%We may want to consider moderating all of this so that the matrix
%multiplation gives us to *matrices* to multiply together....
%imagine:

%Rows represent CUES or STATES, Cols represent ACTIONS; 
C=[0.2 0.99; 
    1 0]; %cues-action mapping
Psi=[0 1; 1 0]; %state-action mapping


psi=[0 1]; %present states

c=[0.1 0];   %present cues
%here, because only cue 1 is present, I'd expect actions based on the FIRST
%ROW, i.e., 0.02, 0.099
c*C

c=[0 0.5];   %present cue 2
c*C % 0.5 0

% now what if BOTH CUES are present!
c=[0.9 0.9];   %present cue 2
c*C %we're really going for it!

%so the same principles will apply to psi*Psi
%how to combine the two sets of vectors together?
(c*C).*(psi*Psi)
%great! I am not sure this is best, but it's what I've been aiming for.

%bonus: what if we were to multiply the matrices directly together, then
%weight?
%Case 1, easy case: cue 1 maps to action 1; cue 2 maps to action 2
%and state 1 maps to action 1; state 2 maps to action 2, but only in that
%exact combination
C=[1 0; 
    0 1]; %cues-action mapping
Psi=[1 0; 
    0 1]; %state-action mapping
C*Psi
%now under different specific presence of absence of cues.
c=[1 0];psi=[1 0];
c.*(C*Psi).*psi %Action 1 activates. great.
c=[0 1];psi=[0 1];
c.*(C*Psi).*psi %action 2 activates
c=[1 0];psi=[0 1];
c.*(C*Psi).*psi %action 2 activates
c=[1 0];psi=[1 1];
c.*(C*Psi).*psi %action 2 activates
c=[1 1];psi=[1 1];
c.*(C*Psi).*psi 
c=[0 0];psi=[1 1];
c.*(C*Psi).*psi 

%what about: same as above, but presence of Cue 2 actually inhibits action 1
%being positive.
%R,C, ROWS ARE CUES/STATES, COLS ARE ACTIONS
C=[1 0; 
    -1 1]; %cues-action mapping
Psi=[1 0; 
    0 1]; %state-action mapping

c=[1 0];psi=[1 0];
(c.*psi)*(C*Psi)
c=[0 1];psi=[0 1];
(c.*psi)*(C*Psi)
c=[1 0];psi=[0 1];
(c.*psi)*(C*Psi)
c=[1 0];psi=[1 1];
(c.*psi)*(C*Psi)
c=[1 1];psi=[1 1];
(c.*psi)*(C*Psi)
c=[0 0];psi=[1 1];
(c.*psi)*(C*Psi)
%THIS IS A METHOD THAT I WOULD LIKE TO PROCEED WITH BUT I DON'T KNOW IF I
%NEED IT JUST YET. WE CAN LOOK INTO THIS.

