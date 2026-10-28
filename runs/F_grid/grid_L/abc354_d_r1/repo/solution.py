import sys


def sigma(i, j):
    # only for i+j even: +1 if black, -1 if white
    c = (i + (i + j) // 2 + j // 2) % 2
    return 1 if c == 0 else -1


# T[a][b] = sum over i<a, j<b (i+j even) of sigma; pattern has period 4 in i and j
T = [[0] * 5 for _ in range(5)]
for a in range(5):
    for b in range(5):
        s = 0
        for i in range(a):
            for j in range(b):
                if (i + j) % 2 == 0:
                    s += sigma(i, j)
        T[a][b] = s


def f(X, Y):
    # X, Y >= 0
    qx, rx = divmod(X, 4)
    qy, ry = divmod(Y, 4)
    return qx * qy * T[4][4] + qx * T[4][ry] + qy * T[rx][4] + T[rx][ry]


def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    OFF = 4 * 10**9
    a, b, c, d = A + OFF, B + OFF, C + OFF, D + OFF
    S = f(c, d) - f(a, d) - f(c, b) + f(a, b)
    print((C - A) * (D - B) + S)


if __name__ == "__main__":
    main()
