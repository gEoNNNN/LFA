import random


class Grammar:
    def __init__(self, vn, vt, p, s):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.S = s

    def generate_strings(self):
        words = []
        while (len(words) != 5):
            str = "S"
            while str.lower() != str:
                str = str.replace(str[len(str) - 1],
                                  p[str[len(str) - 1]][random.randint(0, len(p[str[len(str) - 1]]) - 1)])
            if str not in words:
                words.append(str)
        return words

    def to_finite_automaton(self):
        states = self.Vn + ['X']  # Add accept state X
        alphabet = self.Vt
        transition_function = {}
        transition_function['X'] = {}
        start = self.S
        accept = ['X']

        for non_terminal in self.Vn:
            transition_function[non_terminal] = {}
            for production in self.P.get(non_terminal, []):
                if len(production) == 1:  # Terminal symbol leading to accept state
                    transition_function[non_terminal][production] = 'X'
                elif len(production) == 2:  # Terminal symbol followed by a non-terminal
                    transition_function[non_terminal][production[0]] = production[1]

        return FiniteAutomaton(states, alphabet, transition_function, start, accept)


class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start = start
        self.accept = accept

    def print_automaton(self):
        print('States:', self.states)
        print('Alphabet:', self.alphabet)
        print('Transition function:', self.transition_function)
        print('Start state:', self.start)
        print('Accept state:', self.accept, '\n')

    def is_word_accepted(self, word):
        current_state = self.start
        for char in word:
            if char in self.transition_function.get(current_state, {}):
                current_state = self.transition_function[current_state][char]
            else:
                return False
        return current_state in self.accept


if __name__ == "__main__":
    vn = ['S', 'A', 'B', 'C']
    vt = ['a', 'b']
    p = {
        'S': ['aA'],
        'A': ['bB'],
        'B': ['aA', 'bB'],
        'C': ['bB'],
    }
    s = 'S'

    grammar = Grammar(vn, vt, p, s)

    generated_words = grammar.generate_strings()
    print("\nGenerated strings using the grammar from variant 1:")
    print(generated_words)
    print()

    print("\nFinite Automaton converted from the given grammar:")
    grammar.to_finite_automaton().print_automaton()

    print("\nCheck if the 5 words generated were obtained correctly:")
    for i in generated_words:
        print(i, '-', grammar.to_finite_automaton().is_word_accepted(i))
    print()

    print("\nCheck if random words are evaluated correctly:")
    random_words = ['random', 'VictorBostan10LaLaborator', 'LFAIsCool', 'aecfafafac']
    for i in random_words:
        print(i, '-', grammar.to_finite_automaton().is_word_accepted(i))
    print()

"""
import random


class Grammar:
    def init(self, vn, vt, p, s):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.S = s

    def generate_strings(self):
        results = []
        while len(results) < 5:
            str = self.S
            str = str.replace('S', random.choice(self.P[self.S]))

            while any(nt in str for nt in self.Vn):
                for nt in self.Vn:
                    if nt in str:
                        str = str.replace(nt, random.choice(self.P[nt]), 1)
                        break
            if str not in results:
                results.append(str)

        return results



    def to_finite_automaton(self):
        states = self.Vn + ['X']  # Add accept state X
        alphabet = self.Vt
        transition_function = {}
        transition_function['X'] = {}
        start = self.S
        accept = ['X']

        for non_terminal in self.Vn:
            transition_function[non_terminal] = {}
            for production in self.P.get(non_terminal, []):
                if len(production) == 1:  # Terminal symbol leading to accept state
                    transition_function[non_terminal][production] = 'X'
                elif len(production) == 2:  # Terminal symbol followed by a non-terminal
                    transition_function[non_terminal][production[0]] = production[1]

        return FiniteAutomaton(states, alphabet, transition_function, start, accept)


class FiniteAutomaton:
    def init(self, states, alphabet, transition_function, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start = start
        self.accept = accept

    def print_automaton(self):
        print('States:', self.states)
        print('Alphabet:', self.alphabet)
        print('Transition function:', self.transition_function)
        print('Start state:', self.start)
        print('Accept state:', self.accept, '\n')

    def is_word_accepted(self, word):
        current_state = self.start
        for char in word:
            if char in self.transition_function.get(current_state, {}):
                current_state = self.transition_function[current_state][char]
            else:
                return False
        return current_state in self.accept

    def is_word_accepted(self, word):
        current_state = self.start
        for char in word:
            if char in self.transition_function.get(current_state, {}):
                current_state = self.transition_function[current_state][char]
            else:
                return False
        return current_state in self.accept

if name == "main":
    vn = ['S', 'P', 'Q']
    vt = ['a', 'b', 'c', 'd', 'e', 'f']
    p = {
        'S': ['aP', 'bQ'],
        'P': ['bP', 'cP', 'dQ', 'e'],
        'Q': ['eQ', 'fQ', 'a']
    }
    s = 'S'

    grammar = Grammar(vn, vt, p, s)

    generated_words = grammar.generate_strings()
    print("\nGenerated strings using the grammar from variant 1:")
    print(generated_words)
    print()

    print("\nFinite Automaton converted from the given grammar:")
    grammar.to_finite_automaton().print_automaton()

    print("\nCheck if the 5 words generated were obtained correctly:")
    for i in generated_words:
        print(i, '-', grammar.to_finite_automaton().is_word_accepted(i))
    print()

    print("\nCheck if random words are evaluated correctly:")
    random_words = ['random', 'VictorBostan10LaLaborator', 'LFAIsCool', 'aecfafafac']
    for i in random_words:
        print(i, '-', grammar.to_finite_automaton().is_word_accepted(i))
    print()
"""