import random


def tokenizer(reg_exp):
    tokens = []
    pre_tokens = []
    triggers = ['*', '+', '?', '^']
    temp = ''

    # Split regex by brackets
    reg_exp = reg_exp.replace('(', '%(').replace(')', ')%')
    reg_exp = reg_exp.strip('%').replace('%%', '%')
    print(reg_exp)
    pre_tokens = reg_exp.split('%')

    # Moves the number of repetitions specifiers from an element to the previous element
    for i in range(1, len(pre_tokens)):
        if pre_tokens[i][0] in triggers:
            if pre_tokens[i][0] == '^':
                pre_tokens[i - 1] += pre_tokens[i][0] + pre_tokens[i][1]
                pre_tokens[i] = pre_tokens[i][2:]
            else:
                pre_tokens[i - 1] += pre_tokens[i][0]
                pre_tokens[i] = pre_tokens[i][1:]

    # Checks each pre token to build the tokens
    for pre_token in pre_tokens:
        if pre_token:
            if pre_token[0] == '(':
                if pre_token[len(pre_token) - 2] == '^':
                    temp = pre_token[1:-3]
                    tup = (pre_token[len(pre_token) - 1], temp.split('|'))
                    tokens.append(tup)
                else:
                    if pre_token[len(pre_token) - 1] in triggers:
                        temp = pre_token[1:-2]
                        tup = (pre_token[len(pre_token) - 1], temp.split('|'))
                        tokens.append(tup)
                    else:
                        temp = pre_token[1:-1]
                        tup = ('1', temp.split('|'))
                        tokens.append(tup)
            else:
                temp = ''
                skip = False
                for i, char in enumerate(pre_token):
                    if not skip:
                        if char not in triggers:
                            temp += char
                        else:
                            if char == '^':
                                tokens.append((pre_token[i + 1], [temp]))
                                temp = ''
                                skip = True
                            else:
                                tokens.append((char, [temp]))
                                temp = ''
                    else:
                        skip = False
                if temp:
                    tokens.append(('1', [temp]))

    return tokens


# Function to generate strings based on provided regular expression patterns
def generate_strings(reg_exp, n, limit):
    strings = []  # List to store the generated strings

    for i in range(n):
        string = ''  # Initialize the string to be built
        # Iterate through each token in the regular expression
        for tup in reg_exp:
            if tup[0] == '1':  # '1' denotes a mandatory symbol
                string += random.choice(tup[1])
            elif tup[0] == '?':  # '?' denotes an optional symbol
                nr = random.randint(0, 1)
                if nr:
                    string += random.choice(tup[1])
            elif tup[0] == '+':  # '+' denotes one or more repetitions of a symbol
                char = random.choice(tup[1])
                nr_of_chars = random.randint(1, limit)
                for j in range(nr_of_chars):
                    string += char
            elif tup[0] == '*':  # For other types, assume '*', denoting zero or more repetitions
                char = random.choice(tup[1])
                nr_of_chars = random.randint(0, limit)
                for j in range(nr_of_chars):
                    string += char
            else:  # The case when we have ^5 for example
                char = random.choice(tup[1])
                for j in range(int(tup[0])):
                    string += char

        strings.append(string)

    return strings


# Function to generate a string with a step-by-step explanation
def generate_string_with_explanation(exp, reg_exp, n, limit):
    string = ''
    step = 1  # Step counter for explanation
    print(f'\nGenerating a string for Regular Expression {exp}:\n')
    print(f'Step-by-step explenation:')

    for tup in reg_exp:
        l = len(tup[1])  # Get the number of options for the current component
        if tup[0] == '1':
            string += random.choice(tup[1])
            if l == 1:
                print(f'Step {step}. Append 1 instance of the symbol "{tup[1][0]}". String = {string}')
                step += 1
            else:
                print(
                    f'Step {step}. Append 1 instance of one of these symbols - {", ".join(tup[1])}. String = {string}')
                step += 1
        elif tup[0] == '?':
            nr = random.randint(0, 1)
            print(
                f'Step {step}. Generate a random number between 0 and 1 to determine if a symbol is going to be appended. Generated number = {nr}')
            step += 1
            if nr:
                string += random.choice(tup[1])
                if l == 1:
                    print(f'Step {step}. Append 1 instance of the symbol "{tup[1][0]}". String = {string}')
                    step += 1
                else:
                    print(
                        f'Step {step}. Append 1 instance of one of these symbols - {", ".join(tup[1])}. String = {string}')
                    step += 1
            else:
                print(f'Step {step}. Nothing is being appended. String = {string}')
                step += 1
        elif tup[0] == '+':
            char = random.choice(tup[1])
            nr_of_chars = random.randint(1, limit)
            print(
                f"Step {step}. Generate how many symbols will be appended between 1 and the limit, which is {limit}. In this case we append {nr_of_chars} symbols")
            step += 1
            for j in range(nr_of_chars):
                string += char
            if l == 1:
                print(f'Step {step}. Append {nr_of_chars} instances of the symbol "{tup[1][0]}". String = {string}')
                step += 1
            else:
                print(
                    f'Step {step}. Append {nr_of_chars} instances of one of these symbols - {", ".join(tup[1])}. String = {string}')
                step += 1
        elif tup[0] == '*':
            char = random.choice(tup[1])
            nr_of_chars = random.randint(0, limit)
            print(
                f'Step {step}. Generate how many symbols will be appended between 0 and the limit, which is {limit}. In this case we append {nr_of_chars} symbols')
            step += 1
            for j in range(nr_of_chars):
                string += char
            if l == 1:
                print(f'Step {step}. Append {nr_of_chars} instances of the symbol "{tup[1][0]}". String = {string}')
                step += 1
            else:
                print(
                    f'Step {step}. Append {nr_of_chars} instances of one of these symbols - {", ".join(tup[1])}. String = {string}')
                step += 1
        else:
            char = random.choice(tup[1])
            for j in range(int(tup[0])):
                string += char
            if l == 1:
                print(f'Step {step}. Append {int(tup[0])} instances of the symbol "{tup[1][0]}". String = {string}')
                step += 1
            else:
                print(
                    f'Step {step}. Append {int(tup[0])} instances of one of these symbols - {", ".join(tup[1])}. String = {string}')
                step += 1

    print(f'\nThe resulting string is: {string}')


# Define example regular expressions and their tokenized forms
reg_expressions = [
    '(a|b)(c|d)E⁺G?',
    'P(Q|R|S)T(UV|W|X)*Z⁺',
    '1(0,1)*2(3|4)⁵36'
]
reg_expressions_tokens = [  # Regular expressions tokens
    [('1', ['a', 'b']), ('1', ['c', 'd']), ('+', ['E']), ('?', ['G'])],
    [('1', ['P']), ('1', ['Q', 'R', 'S']), ('1', ['T']), ('*', ['UV', 'W', 'X']), ('+', ['Z'])],
    [('1', ['1']), ('*', ['0', '1']), ('1', ['2']), ('5', ['3', '4']), ('1', ['36'])]
]
limit = 5  # Limit for symbols written an undefined number of times
n = 5  # Number of strings to generate

# for i in range(len(reg_expressions_tokens)):
#     print(f'{n} random strings for Regular Expression {reg_expressions[i]}:')
#     print(generate_strings(reg_expressions_tokens[i], n, limit), '\n')

# generate_string_with_explanation(reg_expressions[1], reg_expressions_tokens[1], n, limit)

# P(Q|R|S)*T(UV|W|X)^4Z+F?(a|b)  (a|b)(c|d)E+G?  1(0,1)*2(3|4)^536  P(Q|R|S)*T(UV|W|X)^4Z+F?(a|b)L^9(b|C|D)+  J+K(L|M|N)*O?(P|Q)^3

temp = '(a|b)(c|d)E+G?'
tokens = tokenizer(temp)
print(f'Tokens for {temp}:\n{tokens}')
# print(generate_strings(tokens, n, limit))
# generate_string_with_explanation(temp, tokens, n, limit)