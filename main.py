NAN = '<not a number>'

DIGITS = '0123456789'
DOT = '.'

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


def get_ast(tokens):
    if not tokens:
        return None
    elif len(tokens) == 1:
        return to_number(tokens[0])
    nodes = []
    operators_stack = []
    for token in tokens:
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
            if char in OPERATORS:
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


if __name__ == '__main__':
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
