
NAN = '<not a number>'

DIGITS = {'0123456789'[i]: i for i in range(10)}


def to_number(s):
    if not s:
        return NAN
    result = 0
    for char in s:
        if char not in DIGITS:
            return NAN
        result = result*10 + DIGITS[char]
    return result


if __name__ == '__main__':
    print('Calculator')
    while True:
        line = input('>>> ')
        if not line:
            break
        number = to_number(line)
        print('line is "%s" of type %s' % (number, type(number)))
    print('done!')
