def check_word_fits_grammar(word):
    vn = ['S', 'A', 'B', 'C']
    vt = ['a', 'b']
    p = {
        'S': ['aA', 'aB'],
        'A': ['bS', ''],  # Include an empty production for A
        'B': ['aC'],
        'C': ['a', 'bS', ''],  # Include an empty production for C
    }
    s = 'S'

    def check_recursive(symbol, remaining_word):
        if not remaining_word:
            return symbol == '' or symbol in vt  # Check if the symbol can transition to an empty string or is terminal
        if symbol in vt:  # If symbol is terminal, it should match the first character of the word
            return remaining_word.startswith(symbol)
        for production in p.get(symbol, []):
            if production == '':  # Handle ε-transition
                if check_recursive('', remaining_word):
                    return True
            elif check_recursive(production[0], remaining_word) and check_recursive(production[1:], remaining_word):
                return True
        return False

    return check_recursive(s, word)

# Test the function
words_to_check = ['aaa', 'aba', 'ab', 'aab']
for word in words_to_check:
    print(f'{word} fits the grammar: {check_word_fits_grammar(word)}')
q0 --(a)--> q1
q0 --(b)--> q2
q1 --(a)--> q3
q1 --(b)--> q4
q2 --(a)--> q5
q2 --(b)--> q6
q3 --(a)--> q7
q3 --(b)--> q8
q4 --(a)--> q9
q4 --(b)--> q10
q5 --(a)--> q11
q5 --(b)--> q4
q6 --(a)--> q3
q6 --(b)--> q8
q7 --(a)--> q11
q7 --(b)--> q10
q8 --(a)--> q7
q8 --(b)--> q8
q9 --(a)--> q3
q9 --(b)--> q10
q10 --(a)--> q5
q10 --(b)--> q8
q11 --(a)--> q11
q11 --(b)--> q11
S : ['aA' ,'bB'].
A : ['bC','bC']*