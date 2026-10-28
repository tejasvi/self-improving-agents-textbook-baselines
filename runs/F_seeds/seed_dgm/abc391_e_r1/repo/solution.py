import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    m = 3 ** n
    # c0[i] / c1[i]: min flips to make node i evaluate to 0 / 1
    c0 = [0 if ch == '0' else 1 for ch in s[:m]]
    c1 = [1 if ch == '0' else 0 for ch in s[:m]]
    length = m
    while length > 1:
        new0 = []
        new1 = []
        for i in range(0, length, 3):
            x = sorted((c0[i], c0[i + 1], c0[i + 2]))
            y = sorted((c1[i], c1[i + 1], c1[i + 2]))
            new0.append(x[0] + x[1])
            new1.append(y[0] + y[1])
        c0, c1 = new0, new1
        length //= 3
    # Flipping the root requires making it the opposite of its current value.
    if c0[0] == 0:
        print(c1[0])
    else:
        print(c0[0])


main()
