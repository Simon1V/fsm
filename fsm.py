import re
import sys
import pygraphviz as pgv

#reserved_symbols = ["d", "(", ",", ")", "->"]

regex_valid_transition_rule = r"d\(q[0-9]+,[a-zA-Z0-9]{1}\)->q[0-9]+"
regex_valid_transition_group_rule = "d\((q[0-9]+),([a-zA-Z0-9]{1})\)->(q[0-9]+)"

def main():
	dot=pgv.AGraph(directed=True)
	dot.edge_attr.update(splines="curved")
	automata = ["d(q0,s)->q1", "d(q0,t)->q0", "d(q1,t)->q0", "finals:q1", "initials:q0"]
	automata2 = ["d(q0,s)->q1", "d(q0,t)->q0", "d(q1,t)->q0", "d(q1, w)-> q2", "d(q2, t) -> q2", "d(q2, s) -> q3", "d(q3, w)->q0" , "finals:q1", "initials:q0, q2"]
	#automata2 = ["d(q0,s)->q3", "d(q0,t)->q0", "d(q1,t)->q0", "d(q1, w)-> q2", "d(q2, t) -> q2", "d(q2, s) -> q3", "d(q3, w)->q0" , "finals:q1", "initials:q0, q2"]


	transition_table = None
	# currently not needed.
	# initials = get_initials(automata2[-1])
	finals = get_finals(automata2[-2])
	automata2 = automata2[:-2]
	# alternatively: use recursive algo or add all nodes first and then transitions.
	for transition in automata2:
		transition_triple = get_entry(transition)
		current_node = transition_triple[0]
		transition_symbol = transition_triple[1]
		target_node = transition_triple[2]
		# add nodes + transitions
		if not dot.has_node(current_node):
			# case decision: is final node or not?
			if current_node in finals:
				dot.add_node(current_node, shape="doublecircle")
			else:
				dot.add_node(current_node)
			# add transitions
			if current_node == target_node:
				dot.add_edge(current_node, target_node, xlabel=transition_symbol, fontsize="10")
			else:
				if not dot.has_node(target_node):
					if target_node  in finals:
						dot.add_node(target_node, shape="doublecircle")
					else:
						dot.add_node(target_node)
				dot.add_edge(current_node, target_node, xlabel=transition_symbol, fontsize="10")

		# add only transitions for existing node (the target node might still not exist)
		else:
			if not dot.has_node(target_node):
				if target_node in finals:
					dot.add_node(target_node, shape="doublecircle")
				else:
					dot.add_node(target_node)
			dot.add_edge(current_node, target_node, xlabel=transition_symbol, fontsize="10")

	dot.write("file1.dot")
	dot.layout(prog="dot")
	dot.graph_attr['dpi'] = '200'
	dot.graph_attr["nodesep"]="1.0"
	options = {
    'node_color': 'black',
    'node_size': 100,
    'width': 3,}
	dot.draw('file1.png')

def get_initials(initials:str)->list:
	trimmed = initials.replace(" ", "")
	initial_states_ = trimmed.split(":")[1]
	initial_states = initial_states_.split(",")
	assert(len(initial_states) > 0)
	return initial_states


def get_finals(finals:str)->list:
	trimmed = finals.replace(" ", "")
	final_states_ = trimmed.split(":")[1]
	final_states = final_states_.split(",")
	assert(len(final_states) > 0)
	return final_states


def get_entry(transition:str) -> list:
	trimmed_tokens = transition.replace(" ", "")
	assert(len(trimmed_tokens) > 0)
	matches = re.search(re.compile(regex_valid_transition_group_rule), trimmed_tokens)
	if matches == None:
		print("Invalid rule specified")
		sys.exit(-1)
	node_src = matches.group(1)
	input_symbol = matches.group(2)
	node_destination = matches.group(3)
	return [node_src, input_symbol, node_destination]


if __name__ == "__main__":
	main()
