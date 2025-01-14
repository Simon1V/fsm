Given an automata described by a list of transition rules 

automata2 = ["d(q0,s)->q1", 
"d(q0,t)->q0", 
"d(q1,t)->q0", 
"d(q1, w)-> q2", 
"d(q2, t) -> q2", 
"d(q2, s) -> q3", 
"d(q3, w)->q0" , 
"finals:q1", 
"initials:q0, q2"]

where each entry is a transition 
transition(current_state, input_symbol) -> target_state

![file1](https://github.com/user-attachments/assets/856a21b0-8f99-44b1-b7d6-39212720fc0a)


such a dot graph will be created with the fsm as graphical representation
