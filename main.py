NAN = '<not a number>'

DIGITS = '0123456789'
OPERATORS = '+'

DIGITS_MAP = {c: i for i, c in enumerate(DIGITS)}


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


class ASTPlus(ASTNode):
    def __init__(self, left_op, right_op):
        """
        :type left_op: ASTNode
        :type right_op: ASTNode
        """
        self.left_op = left_op
        self.right_op = right_op

    def __repr__(self):
        return '[%r `+` %r]' % (self.left_op, self.right_op)

    def calc(self):
        return self.left_op.calc() + self.right_op.calc()


def get_ast(tokens):
    if not tokens:
        return None
    res = to_number(tokens[0])
    for i, action in enumerate(tokens[:-1]):
        if action in OPERATORS:
            res = ASTPlus(res, to_number(tokens[i + 1]))
    return res


def get_tokens(s):
    result = []
    string = ''
    for char in s:
        if char in DIGITS:
            string += char
        else:
            if string:
                result.append(string)
            if char in OPERATORS:
                result.append(char)
            string = ''

    if string:
        result.append(string)

    return result


def to_number(s):
    if not s:
        return NAN
    result = 0
    for char in s:
        if char not in DIGITS_MAP:
            return NAN
        result = result * 10 + DIGITS_MAP[char]
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
