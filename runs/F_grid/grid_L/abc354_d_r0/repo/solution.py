import sys


def g(i, j):
    # doubled black area of unit square [i,i+1]x[j,j+1]
    if (i + j) % 2 == 1:
        return 1
    # uniform square: black iff floor(x)+floor(y/2)+floor((x+y)/2) is even
    f = i + (j // 2) + ((i + j) // 2)
    return 2 if f % 2 == 0 else 0


# 4x4 periodic table and prefix sums
G = [[g(i, j) for j in range(4)] for i in range(4)]
pre = [[0] * 5 for _ in range(5)]
for a in range(1, 5):
    for b in range(1, 5):
        pre[a][b] = pre[a - 1][b] + pre[a][b - 1] - pre[a - 1][b - 1] + G[a - 1][b - 1]
S = pre[4][4]


def H(X, Y):
    # sum of g over i in [0,X), j in [0,Y), valid for any integers
    p, r = divmod(X, 4)
    q, s = divmod(Y, 4)
    return p * q * S + p * pre[4][s] + q * pre[r][4] + pre[r][s]


def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    print(H(C, D) - H(A, D) - H(C, B) + H(A, B))


if __name__ == "__main__":
    main()
