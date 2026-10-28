import sys


def h(i, j):
    # doubled black area of unit cell [i,i+1]x[j,j+1]
    if (i + j) % 2 == 1:
        return 1
    s = i + j
    col = (i + s // 2 + j // 2) % 2
    return 2 if col == 0 else 0


def _cnt(X, r):
    # count t in [0, X) with t ≡ r (mod 4); for X<0 it is negative count
    # f(X) = floor((X - 1 - r)/4) + 1 for X>0 ; general: floor((X - r + 3)/4) - floor((-r+3)/4)
    return (X - r + 3) // 4 - (3 - r) // 4


def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    total = 0
    for r in range(4):
        ci = _cnt(C, r) - _cnt(A, r)
        if ci == 0:
            continue
        for s in range(4):
            cj = _cnt(D, s) - _cnt(B, s)
            if cj == 0:
                continue
            total += h(r, s) * ci * cj
    print(total)


if __name__ == "__main__":
    main()
