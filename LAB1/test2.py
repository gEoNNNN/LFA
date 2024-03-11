import networkx as nx
import matplotlib.pyplot as plt

# Your grammar
states = ['S', 'AB', 'B', 'X']
alphabet = ['a', 'b']
transition_function = {'S': ['aAB'], 'AB': ['aB', 'bB', 'bX'], 'B': ['aB', 'bX'], 'X': []}
start_state = 'S'
accept_states = ['X']


def create_transition_graph(states, alphabet, transition_function, start_state, accept_states):
    G = nx.DiGraph()

    # Add nodes for each state
    for state in states:
        if state in accept_states:
            # Mark accept states with a double circle (special drawing)
            G.add_node(state, peripheries=2)
        else:
            G.add_node(state)

    # Add edges based on the transition function
    for state, transitions in transition_function.items():
        for transition in transitions:
            symbol, next_state = transition[0], transition[1:]  # Split into symbol and resulting state
            G.add_edge(state, next_state, label=symbol)

    # Draw the graph
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos, nodelist=states, node_size=700)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

    # Draw labels
    labels = {n: n for n in states}
    edge_labels = dict([((u, v,), d['label']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_labels(G, pos, labels, font_size=16)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.axis('off')  # Turn off the axis
    plt.show()  # Display the graph


# Call the function to create and display the graph
create_transition_graph(states, alphabet, transition_function, start_state, accept_states)
