import random
class Grammar:
    def __init__(self, vn, vt, p, s, DFAvn, DFAp):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.S = s
        self.DFAVn = DFAvn
        self.DFAP = DFAp

    def generate_strings(self):
        words = []
        while (len(words) != 5):
            str = "S"
            while str.lower() != str:
                str = str.replace(str[len(str) - 1],
                                  self.P[str[len(str) - 1]][random.randint(0, len(self.P[str[len(str) - 1]]) - 1)])
            if str not in words:
                words.append(str)
        return words

    def to_automaton(self):
        states = self.DFAVn + ['X']
        alphabet = self.Vt
        transition_function = {}
        transition_function['X'] = {}
        start = self.S
        accept = ['X']

        for non_terminal in self.DFAVn:
            transition_function[non_terminal] = {}
            for production in self.DFAP.get(non_terminal, []):
                if len(production) == 1:
                    transition_function[non_terminal][production] = 'X'
                elif len(production) == 2:
                    transition_function[non_terminal][production[0]] = production[1]

        return FiniteAutomaton(states, alphabet, transition_function, start, accept)


class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start = start
        self.accept = accept

    def Check(self, word):
        current_state = self.start
        for char in word:
            if char in self.transition_function.get(current_state, {}):
                current_state = self.transition_function[current_state][char]
            else:
                return False
        return current_state in self.accept


if __name__ == "__main__":
    # DFA
    s = 'S'
    DFAvn = ['S', 'C', 'R']
    vt = ['a', 'b']
    DFAp = {'S': ['aR'], 'C': ['a', 'bS'],'R': ['bS', 'aC']}

    # NFA
    NFAvn = ['S', 'A', 'B', 'C']
    NFAp = {
        'S': ['aA', 'aB'],
        'A': ['bS'],
        'B': ['aC'],
        'C': ['a', 'bS'],
    }
    grammar = Grammar(NFAvn, vt, NFAp, s, DFAvn, DFAp)
    generated_words = grammar.generate_strings()
    print("\nGenerated strings using NFA:")
    print(generated_words)
    print("\nCheck if the words are accepted using DFA:")
    for i in generated_words:
        print(f"{i} - {grammar.to_automaton().Check(i)}")
    print("\nChecking random words:")
    random_words = ['random', 'rege', 'abababababbbbbbbbbb']
    for i in random_words:
        print(f"{i} - {grammar.to_automaton().Check(i)}")
    print()