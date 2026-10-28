import sys


def cell_weight(i, j):
    # twice the black area of the unit cell [i,i+1] x [j,j+1]
    if (i + j) % 2 == 1:
        return 1  # split by a diagonal into two halves, one black
    # uniform colour; colour of point (i+0.5, j+0.5) is
    # floor(x) + floor(y/2) + floor((x+y)/2) mod 2, black when even
    c = (i + j // 2 + (i + j) // 2) % 2
    return 2 if c == 0 else 0


W = [[cell_weight(i, j) for j in range(4)] for i in range(4)]
S16 = sum(sum(r) for r in W)


def G(X, Y):
    # sum of weights over i in [0,X), j in [0,Y), X,Y >= 0
    p, r = divmod(X, 4)
    q, s = divmod(Y, 4)
    total = 0
    # rows i in [0, 4): sum over j in [0, Y)
    row_full = [0] * 4
    for i in range(4):
        v = q * sum(W[i])
        for j in range(s):
            v += W[i][j]
        row_full[i] = v
    total += p * sum(row_full)
    for i in range(r):
        total += row_full[i]
    return total


def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    a1 = A % 4
    a2 = a1 + (C - A)
    b1 = B % 4
    b2 = b1 + (D - B)
    ans = G(a2, b2) - G(a1, b2) - G(a2, b1) + G(a1, b1)
    print(ans)


if __name__ == "__main__":
    main()
