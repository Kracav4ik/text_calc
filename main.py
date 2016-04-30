
NAN = '<not a number>'

DIGITS = {c: i for i, c in enumerate('0123456789')}


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

    def calc(self):
        return self.left_op.calc() + self.right_op.calc()


def to_number(s):
    if not s:
        return NAN
    result = 0
    for char in s:
        if char not in DIGITS:
            return NAN
        result = result*10 + DIGITS[char]
    return ASTNumber(result)


if __name__ == '__main__':
    print('Calculator')
    while True:
        line = input('>>> ')
        if not line:
            break
        value = to_number(line)
        print('line is "%s" of type %s' % (value, type(value)))
    print('done!')
