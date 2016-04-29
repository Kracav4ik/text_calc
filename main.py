

if __name__ == '__main__':
    print('Calculator')
    while True:
        line = input('>>> ')
        if not line:
            break
        print('line is "%s"' % line)
    print('done!')
