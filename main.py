NAN = '<not a number>'

DIGITS = '0123456789'
DOT = '.'
LEFT_PAREN = '('
RIGHT_PAREN = ')'

DIGITS_MAP = {c: i for i, c in enumerate(DIGITS)}

OPERATORS_MAP = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}
OPERATORS = OPERATORS_MAP.keys()
PRIORITY_MAP = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
}


class ASTNode:
    def calc(self):
        pass

    def __str__(self):
        return str(self.calc())


class ASTNumber(ASTNode):
    def __init__(self, number):
        """
        :type number: int
        """
        self.number = number

    def __repr__(self):
        return '[%s]' % self

    def calc(self):
        return self.number


class ASTOperator(ASTNode):
    def __init__(self, left_op, right_op, op):
        """
        :type left_op: ASTNode
        :type right_op: ASTNode
        :type op: str
        """
        self.left_op = left_op
        self.right_op = right_op
        self.op = op

    def __repr__(self):
        return '[%r `%s` %r]' % (self.left_op, self.op, self.right_op)

    def calc(self):
        return OPERATORS_MAP[self.op](self.left_op.calc(), self.right_op.calc())


class ASTParens(ASTNode):
    def __init__(self, subtree):
        """
        :type subtree: ASTNode
        """
        self.subtree = subtree

    def __repr__(self):
        return '( %r )' % self.subtree

    def calc(self):
        return self.subtree.calc()


def get_ast(tokens):
    if not tokens:
        return None
    elif len(tokens) == 1:
        return to_number(tokens[0])
    nodes = []
    operators_stack = []
    token_idx = 0
    while token_idx < len(tokens):
        token = tokens[token_idx]
        token_idx += 1
        # print('* token %s' % token)
        if token in OPERATORS:
            while operators_stack:
                last_op = operators_stack[-1]
                if PRIORITY_MAP[token] > PRIORITY_MAP[last_op]:
                    # print('* stopping because `%s` has more prio than `%s`' % (token, last_op))
                    break
                new_node = ASTOperator(nodes[-2], nodes[-1], last_op)
                # print('* merging %r and %r to %r' % (nodes[-2], nodes[-1], new_node))
                nodes = nodes[:-2]
                operators_stack = operators_stack[:-1]
                nodes.append(new_node)
            operators_stack.append(token)
            # print('* op stack is', operators_stack)
        elif token == LEFT_PAREN:
            paren_level = 0
            left_paren_idx = token_idx - 1
            local_i = left_paren_idx
            while local_i < len(tokens):
                local_token = tokens[local_i]
                local_i += 1
                if local_token == LEFT_PAREN:
                    paren_level += 1
                elif local_token == RIGHT_PAREN:
                    paren_level -= 1
                    if paren_level == 0:
                        right_paren_idx = local_i - 1
                        break

            nodes.append(ASTParens(get_ast(tokens[left_paren_idx + 1:right_paren_idx])))
            token_idx = right_paren_idx + 1
        else:
            nodes.append(to_number(token))
    while operators_stack:
        new_node = ASTOperator(nodes[-2], nodes[-1], operators_stack[-1])
        # print('* merging %r and %r to %r' % (nodes[-2], nodes[-1], new_node))
        nodes = nodes[:-2]
        operators_stack = operators_stack[:-1]
        nodes.append(new_node)
    return nodes[0]


def get_tokens(s):
    result = []
    string = ''
    bull = True
    for char in s:
        if char in DIGITS:
            string += char
        elif char == DOT and bull:
            string += char
            bull = False
        else:
            if string and string != DOT:
                result.append(string)
                bull = True
            if char in OPERATORS or char == RIGHT_PAREN or char == LEFT_PAREN:
                result.append(char)
            string = ''

    if string and string != DOT:
        result.append(string)

    return result


def to_number(s):
    if not s:
        return NAN
    result_before_dot = 0
    result_after_dot = 0

    for char in s:
        if char not in DIGITS_MAP and char != DOT:
            return NAN
        if char == DOT:
            break
        result_before_dot = result_before_dot * 10 + DIGITS_MAP[char]
    if DOT in s:
        for char in s[::-1]:
            if char == DOT:
                break
            result_after_dot = result_after_dot / 10 + DIGITS_MAP[char]
        result_after_dot /= 10
    result = result_before_dot + result_after_dot
    return ASTNumber(result)


def self_test():
    assert get_tokens('') == []
    assert get_tokens('123') == ['123']
    assert get_tokens('   1  + 2  ') == ['1', '+', '2']
    assert get_tokens('(+(+(+(+') == ['(', '+', '(', '+', '(', '+', '(', '+']

    assert repr(get_ast(get_tokens('1+2*3'))) == '[[1] `+` [[2] `*` [3]]]'
    assert repr(get_ast(get_tokens('2.'))) == '[2.0]'
    assert repr(get_ast(get_tokens('2.1'))) == '[2.1]'
    assert repr(get_ast(get_tokens('.1'))) == '[0.1]'
    assert repr(get_ast(get_tokens('.1+2.'))) == '[[0.1] `+` [2.0]]'
    assert repr(get_ast(get_tokens('1+(2+3)'))) == '[[1] `+` ( [[2] `+` [3]] )]'
    assert repr(get_ast(get_tokens('1+(2+3)*4'))) == '[[1] `+` [( [[2] `+` [3]] ) `*` [4]]]'


if __name__ == '__main__':
    self_test()
    print('Calculator')
    while True:
        line = input('>>> ')
        if not line:
            break
        tokens = get_tokens(line)
        print('tokens:', tokens)
        value = get_ast(tokens)
        print('tree is %r' % value)
        print('value is "%s" of type %s' % (value, type(value)))
    print('done!')
