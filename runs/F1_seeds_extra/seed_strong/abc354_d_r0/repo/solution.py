import sys


def cell_value(i, j):
    # twice the black area of the unit cell [i,i+1]x[j,j+1]
    if (i + j) % 2 == 1:
        # cell is split by a line x+y = even integer into two equal halves of opposite colors
        return 1
    # uniform cell: color parity of floor(x) + floor(y/2) + floor((x+y)/2) at the center
    color = (i + j // 2 + (i + j + 1) // 2) % 2
    return 2 if color == 0 else 0


def count(lo, hi, r):
    # number of integers k in [lo, hi) with k mod 4 == r
    return (hi - r + 3) // 4 - (lo - r + 3) // 4


def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    v = [[cell_value(r, s) for s in range(4)] for r in range(4)]
    ans = 0
    for r in range(4):
        ci = count(A, C, r)
        for s in range(4):
            ans += ci * count(B, D, s) * v[r][s]
    print(ans)


main()
