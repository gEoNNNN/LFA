import random

def check_nfa(input_dict):
    check = False
    for _, strings in input_dict.items():
        first_letters = [string[0] for string in strings if string]
        if len(set(first_letters)) < len(first_letters):
            check = True
            break
    return check

def nfa_to_dfa(vn, vt, p, s):
    keys = p.keys()
    table1 = {}

    def transform_dict(input_dict):
        for key in list(input_dict.keys()):
            for terminal in list(input_dict[key].keys()):
                temp = [""]
                for symbol in input_dict[key][terminal]:
                    if symbol not in temp[0]:
                        temp[0] += symbol
                input_dict[key][terminal] = temp
        return input_dict

    def dict_to_grammar(input_dict):
        grammar = {}
        for key in list(input_dict.keys()):
            grammar[key] = []
            for terminal in list(input_dict[key].keys()):
                for symbol in input_dict[key][terminal]:
                    production = str(terminal) + str(symbol)
                    if symbol and production not in grammar[key]:
                        grammar[key].append(production)
        for key in list(grammar.keys()):
            for i in range(0,len(grammar[key])):
                if grammar[key][i][1] == 'X':
                    grammar[key][i] = grammar[key][i][:-1]
        for key in list(grammar.keys()):
            if len(key)>1:
                newkey = 'S'
                while newkey not in list(grammar.keys()):
                    newkey = chr(random.randint(65, 90))
                grammar[newkey] = grammar.pop(key)
        if 'X' in grammar:
            del grammar['X']
        return grammar

    for key in keys:
        table1[key] = {terminal: [] for terminal in vt}

    for key in keys:
        for production in p[key]:
            if production[0] in vt:
                terminal = production[0]
                if len(production) == 1:
                    table1[key][terminal].append("X")
                else:
                    for char in production[1:]:
                        if char in vn:
                            table1[key][terminal].append(char)

    table1 = transform_dict(table1)
    table2 = {'S': table1['S']}
    check = False
    prevlen = 0
    while not check:
        keys = list(table2.keys())
        if prevlen == len(keys):
            check = True
        else:
            prevlen = len(keys)

        for key in keys:
            for terminal in table2[key]:
                potential_key = table2[key][terminal]
                if potential_key and potential_key[0] and potential_key[0] not in keys:
                    if len(potential_key[0]) == 1:
                        table2[potential_key[0]] = table1.get(potential_key[0], {t: [] for t in vt})
                    else:
                        temp = {t: [] for t in vt}
                        for letter in potential_key[0]:
                            if letter in table1:
                                terminalkeys = table1[letter].keys()
                                for k in terminalkeys:
                                    for i in table1[letter][k]:
                                        if i and i not in temp[k]:
                                            temp[k].append(i)
                        table2[potential_key[0]] = temp
    return dict_to_grammar(table2)

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
