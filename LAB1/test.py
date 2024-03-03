import random

def check_nfa(input_dict):
    check = False
    for _, strings in input_dict.items():
        first_letters = [string[0] for string in strings if string]
        if len(set(first_letters)) < len(first_letters):
            check = True
            break
    return check

class Grammar:
    def __init__(self, vn, vt, p, s):
        self.Vn = vn
        self.Vt = vt
        self.P = p
        self.S = s

    def generate_strings(self):
        words = []
        while len(words) != 5:
            str = self.S
            while str.lower() != str:
                if str[len(str)-1] == 'X':
                    str = str[:-1]
                    break
                nont_erminal = ''.join([char for char in str if char.isupper()])
                str = str.replace(nont_erminal,self.P[nont_erminal][random.randint(0, len(self.P[nont_erminal]) - 1)])
            if str not in words:
                words.append(str)
        return words

    def to_automaton(self):
        states = self.Vn + ['X']
        alphabet = self.Vt
        transition_function = {}
        transition_function['X'] = {}
        start = self.S
        accept = ['X']

        for non_terminal in self.Vn:
            transition_function[non_terminal] = {}
            for production in self.P.get(non_terminal, []):
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
    vn = ['S', 'A', 'B', 'C']
    vt = ['a', 'b']
    #p = {'S': ['aAB'], 'AB': ['aC', 'bS'], 'C': ['a', 'bS']}
    p = {'S': ['aA'], 'A': ['aC', 'bS'], 'C': ['a', 'bS']}
    s = 'S'
    if check_nfa(p) == True:
        p = nfa_to_dfa(vn, vt, p, s)
        print(p)
    grammar = Grammar(vn, vt, p, s)
    generated_words = grammar.generate_strings()
    print("\nGenerated strings using the grammar:")
    print(generated_words)
    print("\nCheck if the words are accepted using the automaton:")
    for i in generated_words:
        print(f"{i} - {grammar.to_automaton().Check(i)}")
    print("\nChecking random words:")
    random_words = ['random', 'rege', 'abababababbbbbbbbbb']
    for i in random_words:
        print(f"{i} - {grammar.to_automaton().Check(i)}")
