import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    m = 3 ** n
    s = s[:m]
    # c0[i]: min changes so that leaf i is 0; c1[i]: so that it is 1
    c0 = [0 if ch == "0" else 1 for ch in s]
    c1 = [1 - x for x in c0]
    for _ in range(n):
        nc0 = []
        nc1 = []
        for i in range(0, len(c0), 3):
            a, b, c = c0[i], c0[i + 1], c0[i + 2]
            # sum of two smallest
            nc0.append(a + b + c - max(a, b, c))
            a, b, c = c1[i], c1[i + 1], c1[i + 2]
            nc1.append(a + b + c - max(a, b, c))
        c0, c1 = nc0, nc1
    # exactly one of c0[0], c1[0] is 0 (the current root value);
    # the answer is the cost to force the other value
    print(max(c0[0], c1[0]))


if __name__ == "__main__":
    main()
