from Grammar import GenericGrammar
import unittest

class BreakFromLoops(Exception):
    pass

class CNFGrammar(GenericGrammar):
    def convert_to_cnf(self):
        self.start_symbol_rhs_removal()
        self.remove_empty_productions()
        self.remove_unit_productions()
        self.remove_inaccessible_symbols()
        self.replace_terminals_with_nonterminals()
        self.reduce_production_length()

    def start_symbol_rhs_removal(self):
        try:
            for value in self.P.values():
                for production in value:
                    for character in production:
                        if character == self.S:
                            raise BreakFromLoops
        except:
            new_P = {'X': [self.S]}
            new_P.update(self.P)
            self.P = new_P
            self.S = 'X'
            self.Vn.append(self.S)

    def create_new_productions(self, production, character):
        results = []
        for i in range(len(production)):
            if production[i] == character:
                new_production = production[:i] + production[i+1:]
                results.append(new_production)
        return results

    def remove_empty_productions(self):
        count_empty = 0
        empty_prods = []
        for key, value in self.P.items():
            for production in value:
                if production == 'ε':
                    count_empty += 1
                    empty_prods.append(key)
                    value.remove(production)
        for i in range(count_empty):
            new_P = self.P
            for key, value in self.P.items():
                for production in value:
                    for character in production:
                        if character == empty_prods[i]:
                            new_productions = self.create_new_productions(production, empty_prods[i])
                            for j in new_productions:
                                if j not in new_P[key]:
                                    new_P[key].append(j)
                            break
            self.P = new_P

    def remove_unit_productions(self):
        for key, value in self.P.items():
            for production in value:
                if key == production:
                    self.P[key].remove(production)
        changes = True
        while changes:
            changes = False
            for key, value in self.P.items():
                for production in value:
                    if production in self.Vn:
                        changes = True
                        self.P[key].remove(production)
                        for prod in self.P[production]:
                            if prod not in self.P[key]:
                                self.P[key].append(prod)

    def remove_inaccessible_symbols(self):
        accessible = set([self.S])
        queue = [self.S]

        while queue:
            current = queue.pop(0)
            for production in self.P.get(current, []):
                for symbol in production:
                    if symbol in self.Vn and symbol not in accessible:
                        accessible.add(symbol)
                        queue.append(symbol)

        self.Vn = [nt for nt in self.Vn if nt in accessible]
        for nt in list(self.P.keys()):
            if nt not in accessible:
                del self.P[nt]

    def replace_terminals_with_nonterminals(self):
        def new_nonterminal(existing):
            for char in (chr(i) for i in range(65, 91)):
                if char not in existing:
                    return char
            raise ValueError("Ran out of single-letter nonterminal symbols!")

        terminal_to_nonterminal = {}
        new_P = {}
        for key, productions in self.P.items():
            new_productions = []
            for prod in productions:
                if len(prod) > 1:
                    new_prod = ''
                    for char in prod:
                        if char in self.Vt:
                            if char not in terminal_to_nonterminal:
                                new_nt = new_nonterminal(set(self.Vn) | set(new_P.keys()))
                                self.Vn.append(new_nt)
                                terminal_to_nonterminal[char] = new_nt
                                new_P[new_nt] = [char]
                            new_prod += terminal_to_nonterminal[char]
                        else:
                            new_prod += char
                    new_productions.append(new_prod)
                else:
                    new_productions.append(prod)
            new_P[key] = new_productions
        self.P.update(new_P)

    def reduce_production_length(self):
        def new_nonterminal(existing):
            for char in (chr(i) for i in range(65, 91)):
                if char not in existing:
                    return char
            raise ValueError("Ran out of single-letter nonterminal symbols!")

        existing_binaries = {}
        new_productions_dict = {}
        for key, productions in list(self.P.items()):
            new_productions = []
            for production in productions:
                if len(production) > 2:
                    while len(production) > 2:
                        last_two = production[-2:]
                        if last_two not in existing_binaries:
                            new_nt = new_nonterminal(set(self.Vn) | set(new_productions_dict.keys()))
                            self.Vn.append(new_nt)
                            new_productions_dict[new_nt] = [last_two]
                            existing_binaries[last_two] = new_nt
                        production = production[:-2] + existing_binaries[last_two]
                    new_productions.append(production)
                else:
                    new_productions.append(production)
            self.P[key] = new_productions
        self.P.update(new_productions_dict)

class TestCNFGrammarMethods(unittest.TestCase):
    def setUp(self):
        self.grammar = CNFGrammar(['S', 'A', 'B', 'C', 'D'], ['a', 'b'], {
            'S': ['aB', 'bA', 'B'],
            'A': ['b', 'aD', 'AS', 'bAB', 'ε'],
            'B': ['a', 'bS'],
            'C': ['AB'],
            'D': ['BB']
        }, 'S')

    def test_start_symbol_rhs_removal(self):
        self.grammar.start_symbol_rhs_removal()
        for prod in self.grammar.P.values():
            self.assertNotIn(self.grammar.S, prod)

    def test_remove_empty_productions(self):
        self.grammar.remove_empty_productions()
        for prods in self.grammar.P.values():
            self.assertNotIn('ε', prods)

    def test_remove_unit_productions(self):
        self.grammar.remove_unit_productions()
        for key, prods in self.grammar.P.items():
            for prod in prods:
                self.assertFalse(len(prod) == 1 and prod.isupper())

    def test_remove_inaccessible_symbols(self):
        self.grammar.Vn.append('Z')
        self.grammar.remove_inaccessible_symbols()
        self.assertNotIn('Z', self.grammar.Vn)

    def test_replace_terminals_with_nonterminals(self):
        self.grammar.replace_terminals_with_nonterminals()
        for prods in self.grammar.P.values():
            for prod in prods:
                if len(prod) > 1:
                    self.assertTrue(all(char in self.grammar.Vn for char in prod))

    def test_reduce_production_length(self):
        self.grammar.replace_terminals_with_nonterminals()
        self.grammar.reduce_production_length()
        for prods in self.grammar.P.values():
            for prod in prods:
                self.assertTrue(len(prod) <= 2)

    def test_grammar_print(self):
        self.grammar.convert_to_cnf()
        self.grammar.print_grammar()

if __name__ == '__main__':
    unittest.main()
