import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    length = 3 ** n
    s = s[:length]
    # c0[i], c1[i]: min changes so that the current node's value is 0 / 1
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [1 if ch == '0' else 0 for ch in s]
    for _ in range(n):
        m = len(c0) // 3
        n0 = [0] * m
        n1 = [0] * m
        for i in range(m):
            a, b, c = c0[3 * i], c0[3 * i + 1], c0[3 * i + 2]
            # sum of two smallest
            if a > b:
                a, b = b, a
            if b > c:
                b, c = c, b
            if a > b:
                a, b = b, a
            n0[i] = a + b
            a, b, c = c1[3 * i], c1[3 * i + 1], c1[3 * i + 2]
            if a > b:
                a, b = b, a
            if b > c:
                b, c = c, b
            if a > b:
                a, b = b, a
            n1[i] = a + b
        c0, c1 = n0, n1
    # root value
    if c0[0] == 0:
        # root currently 0 (cost to be 0 is 0); need to make it 1
        print(c1[0])
    else:
        print(c0[0])


main()
