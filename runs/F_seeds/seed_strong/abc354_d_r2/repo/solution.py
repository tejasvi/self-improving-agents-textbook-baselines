import sys


def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    # Shift by a multiple of 4 so all cell indices are non-negative;
    # the pattern has period 4 in both cell-index directions.
    M = 4 * (10 ** 9 // 4 + 1)
    A += M
    C += M
    B += M
    D += M

    def w(i, j):
        if (i + j) % 2 == 1:
            return 1
        c = (i + j // 2 + (i + j) // 2) % 2
        return 2 if c == 0 else 0

    # residue table: P[r][s] = sum over i<r, j<s of w, within [0,4)
    P = [[0] * 5 for _ in range(5)]
    for r in range(5):
        for s in range(5):
            P[r][s] = sum(w(i, j) for i in range(r) for j in range(s))
    T = P[4][4]

    def G(X, Y):
        qx, rx = divmod(X, 4)
        qy, ry = divmod(Y, 4)
        return qx * qy * T + qx * P[4][ry] + qy * P[rx][4] + P[rx][ry]

    ans = G(C, D) - G(A, D) - G(C, B) + G(A, B)
    print(ans)


main()
