
NAN = '<not a number>'

DIGITS = {'0123456789'[i]: i for i in range(10)}


class ASTNode:
    def calc(self):
        pass

    def __str__(self):
        return str(self.calc())


class ASTNumber(ASTNode):
    def __init__(self, number):
        self.number = number

    def calc(self):
        return self.number


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
        number = to_number(line)
        print('line is "%s" of type %s' % (number, type(number)))
    print('done!')
