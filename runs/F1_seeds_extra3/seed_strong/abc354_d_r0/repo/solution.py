import sys


def cnt(hi, lo, r):
    # number of t in [lo, hi) with t % 4 == r, signed
    return -((r - hi) // 4) - (-((r - lo) // 4))


def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    # Unit cell (i, j) = [i,i+1]x[j,j+1].
    # i+j odd: each cell contributes exactly 1 (twice black area of half-triangle).
    # i+j even: whole cell has one color; black => contributes 2.
    # black iff (i + j//2 + (i+j)//2) % 2 == 0 ; periodic mod 4 in i and j.
    val = [[0] * 4 for _ in range(4)]
    for r in range(4):
        for s in range(4):
            if (r + s) % 2 == 1:
                val[r][s] = 1
            else:
                par = (r + s // 2 + (r + s) // 2) % 2
                val[r][s] = 2 if par == 0 else 0
    total = 0
    for r in range(4):
        ci = cnt(C, A, r)
        if ci == 0:
            continue
        for s in range(4):
            cj = cnt(D, B, s)
            total += ci * cj * val[r][s]
    print(total)


main()
