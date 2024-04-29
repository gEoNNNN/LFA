import random

def tokenize_pattern(exp):
    elements = []
    temp_elements = []
    special_chars = ['*', '+', '?', 'ˆ']
    element_builder = ''

    # Modify pattern by adding delimiters
    exp = exp.replace('(', '%(').replace(')', ')%').strip('%').replace('%%', '%')
    temp_elements = exp.split('%')

    # Transfer repetition characters to the preceding elements
    for index in range(1, len(temp_elements)):
        if temp_elements[index][0] in special_chars:
            if temp_elements[index][0] == 'ˆ':
                temp_elements[index - 1] += temp_elements[index][0] + temp_elements[index][1]
                temp_elements[index] = temp_elements[index][2:]
            else:
                temp_elements[index - 1] += temp_elements[index][0]
                temp_elements[index] = temp_elements[index][1:]

    # Construct the final token elements
    for part in temp_elements:
        if part:
            if part[0] == '(':
                if part[-2] == 'ˆ':
                    element_builder = part[1:-3]
                    elements.append((part[-1], element_builder.split('|')))
                else:
                    if part[-1] in special_chars:
                        element_builder = part[1:-2]
                        elements.append((part[-1], element_builder.split('|')))
                    else:
                        element_builder = part[1:-1]
                        elements.append(('1', element_builder.split('|')))
            else:
                element_builder = ''
                skip_char = False
                for idx, char in enumerate(part):
                    if not skip_char:
                        if char not in special_chars:
                            element_builder += char
                        else:
                            if char == 'ˆ':
                                elements.append((part[idx + 1], [element_builder]))
                                element_builder = ''
                                skip_char = True
                            else:
                                elements.append((char, [element_builder]))
                                element_builder = ''
                    else:
                        skip_char = False
                if element_builder:
                    elements.append(('1', [element_builder]))

    return elements

def build_strings(pattern_tokens, count, repeat_limit):
    result_set = []

    for _ in range(count):
        sequence = ''
        for token in pattern_tokens:
            if token[0] == '1':
                sequence += random.choice(token[1])
            elif token[0] in ['?', '+', '*']:
                chars = random.choice(token[1])
                num_chars = random.randint(1, repeat_limit) if token[0] != '*' else random.randint(0, repeat_limit)
                sequence += chars * num_chars
            elif token[0].isdigit():
                chars = random.choice(token[1])
                sequence += chars * int(token[0])

        result_set.append(sequence)

    return result_set

def detail_string_construction(expression, tokens, count, repeat_limit):
    detailed_string = ''
    explanation_step = 1
    print(f'\nDetailed creation from pattern: {expression}\n')
    print('Explanation for each step:')

    for token in tokens:
        num_options = len(token[1])
        choice = random.choice(token[1])
        if token[0].isdigit():
            detailed_string += choice * int(token[0])
            print(f'Step {explanation_step}: Add "{choice}" {token[0]} times. Result: {detailed_string}')
            explanation_step += 1
        else:
            repeats = random.randint(0, repeat_limit) if token[0] == '*' else 1
            detailed_string += choice * repeats
            print(f'Step {explanation_step}: Optionally add "{choice}" up to {repeats} times. Result: {detailed_string}')
            explanation_step += 1

    print(f'\nCompleted string: {detailed_string}')

# Patterns extracted from your input
reg_patterns = [
    '(a|b)(c|d)E⁺G?',
    'P(Q|R|S)T(UV|W|X)*Z⁺',
    '1(0|1)*2(3|4)⁵36'
]

# Processing each pattern
for expression in reg_patterns:
    tokenized_expression = tokenize_pattern(expression)
    print(f'\nTokenized pattern for "{expression}":\n{tokenized_expression}')
    strings_from_pattern = build_strings(tokenized_expression, count=5, repeat_limit=5)
    print(f'Strings from pattern "{expression}":\n{strings_from_pattern}\n')
    for generated_string in strings_from_pattern:
        detail_string_construction(expression, tokenized_expression, count=1, repeat_limit=5)
