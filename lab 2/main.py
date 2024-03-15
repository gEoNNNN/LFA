import networkx as graph
import matplotlib.pyplot as figure

class BaseGrammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.NonTerminals = non_terminals
        self.Terminals = terminals
        self.Productions = productions
        self.StartSymbol = start_symbol

    def display_grammar(self):
        print('Non-terminals:', self.NonTerminals)
        print('Terminals:', self.Terminals)
        print('Productions:', self.Productions)
        print('Start Symbol:', self.StartSymbol, '\n')

    def classify(self):
        is_regular = True
        is_context_free = True
        is_context_sensitive = True

        for lhs, rhs_list in self.Productions.items():
            for rhs in rhs_list:
                # Check for Type 3 (Regular Grammar)
                if not (len(rhs) == 1 and rhs in self.Terminals) and not (len(rhs) == 2 and rhs[0] in self.Terminals and rhs[1] in self.NonTerminals):
                    is_regular = False
                # Check for Type 2 (Context-Free Grammar)
                if len(lhs) != 1 or not lhs.isupper():
                    is_context_free = False
                # Check for Type 1 (Context-Sensitive Grammar)
                if len(rhs) < len(lhs):
                    is_context_sensitive = False

        if is_regular:
            return "Type 3 (Regular Grammar)"
        elif is_context_free:
            return "Type 2 (Context-Free Grammar)"
        elif is_context_sensitive:
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"

class BaseAutomaton:
    def __init__(self, set_of_states, input_alphabet, transition_rules, initial_state, accepting_states):
        self.States = set_of_states
        self.Alphabet = input_alphabet
        self.Transitions = transition_rules
        self.Initial = initial_state
        self.Accepting = accepting_states

    def display_automaton(self):
        print('States:', self.States)
        print('Alphabet:', self.Alphabet)
        print('Transition Rules:', self.Transitions)
        print('Initial State:', self.Initial)
        print('Accepting States:', self.Accepting, '\n')

class Automaton(BaseAutomaton):
    def convert_to_grammar(self):
        non_terminals = self.States
        terminals = self.Alphabet
        start_symbol = self.Initial
        productions = {state: [] for state in non_terminals}

        for state, trans in self.Transitions.items():
            for letter, next_states in trans.items():
                for next_state in next_states:
                    if next_state in self.Accepting:
                        productions[state].append(letter)
                    else:
                        production_rule = letter + next_state
                        productions[state].append(production_rule)

        return BaseGrammar(non_terminals, terminals, productions, start_symbol)

    def transform_nfa_to_dfa(self):
        initial = frozenset([self.Initial])
        unprocessed = [initial]
        dfa_states = {initial}
        dfa_transitions = {}
        dfa_finals = set()

        while unprocessed:
            current = unprocessed.pop()
            dfa_transitions[current] = {}

            for char in self.Alphabet:
                new_state = frozenset(
                    sum([self.Transitions.get(state, {}).get(char, []) for state in current], [])
                )
                if new_state:
                    dfa_transitions[current][char] = new_state
                    if new_state not in dfa_states:
                        dfa_states.add(new_state)
                        unprocessed.append(new_state)
                    if new_state & set(self.Accepting):
                        dfa_finals.add(new_state)

        named_states = {state: ''.join(sorted(state)) for state in dfa_states}
        named_transitions = {
            named_states[state]: {char: named_states[next_state] for char, next_state in edges.items()}
            for state, edges in dfa_transitions.items()
        }
        named_dfa_states = set(named_states.values())
        named_finals = {named_states[state] for state in dfa_finals}
        named_initial = named_states[initial]

        for state in named_dfa_states:
            for key, value in named_transitions[state].items():
                named_transitions[state][key] = [value]

        return Automaton(named_dfa_states, self.Alphabet, named_transitions, named_initial, named_finals)

    def verify_automaton_type(self):
        is_dfa = True
        for _, transitions in self.Transitions.items():
            for _, states in transitions.items():
                if len(states) > 1:
                    is_dfa = False
                    break
        if is_dfa:
            print("\nThis automaton is a DFA!\n")
        else:
            print("\nThis automaton is an NFA!\n")

    def visualize(self):
        Net = graph.DiGraph()
        for state in self.States:
            Net.add_node(state)
        for from_state, trans in self.Transitions.items():
            for input_char, to_states in trans.items():
                for to_state in to_states:
                    Net.add_edge(from_state, to_state, label=input_char)
        layout = graph.spring_layout(Net)
        figure.figure(figsize=(8, 8))
        graph.draw_networkx_nodes(Net, layout, node_size=700, node_color='lightgreen')
        graph.draw_networkx_edges(Net, layout, arrowstyle='-|>', arrowsize=20)
        graph.draw_networkx_labels(Net, layout, font_size=14)
        labels = graph.get_edge_attributes(Net, 'label')
        graph.draw_networkx_edge_labels(Net, layout, edge_labels=labels)
        for node, (x, y) in layout.items():
            for neighbor in Net.neighbors(node):
                if node == neighbor:
                    label = labels[(node, neighbor)]
                    loop_pos = (x, y + 0.1)
                    figure.text(loop_pos[0], loop_pos[1], label, size=12, ha='center', va='center')
        figure.axis('off')
        figure.show()


if __name__ == "__main__":
    set_of_states = ['Q', 'R', 'S', 'T']
    input_alphabet = ['x', 'y', 'z']
    transition_rules = {
        'Q': {'x': ['Q', 'R']},
        'R': {'y': ['S']},
        'S': {'x': ['S'], 'y': ['T']},
        'T': {'x': ['T']}
    }
    initial_state = 'Q'
    accepting_states = ['T']

    automaton = Automaton(set_of_states, input_alphabet, transition_rules, initial_state, accepting_states)
    generated_grammar = automaton.convert_to_grammar()
    generated_grammar.display_grammar()
    print(generated_grammar.classify())
    automaton.verify_automaton_type()
    transformed_dfa = automaton.transform_nfa_to_dfa()
    transformed_dfa.display_automaton()
    transformed_dfa.verify_automaton_type()
    transformed_dfa_grammar = transformed_dfa.convert_to_grammar()
    transformed_dfa_grammar.display_grammar()
    print(transformed_dfa_grammar.classify())
    automaton.visualize()
    transformed_dfa.visualize()
