
def test():
    a = b = [1, 2, 3]

    a.remove(1)

    print(b)

    c = [4,5, 6]
    d = c.copy()

    c.remove(4)
    print(d)


if __name__ == '__main__':
    test()
