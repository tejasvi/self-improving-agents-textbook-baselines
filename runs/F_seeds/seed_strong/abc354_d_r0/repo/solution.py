import sys


def value(i, j):
    # twice the black area inside unit cell [i,i+1]x[j,j+1]
    if (i + j) % 2 == 1:
        return 1  # split by anti-diagonal: exactly one black triangle
    # uniform cell: black iff parity of floor(x)+floor(y/2)+floor((x+y)/2) is even
    f = (i + j // 2 + (i + j) // 2) % 2
    return 2 if f == 0 else 0


def count_res(lo, hi, r):
    # number of integers k in [lo, hi] with k % 4 == r
    return (hi - r) // 4 - (lo - 1 - r) // 4


def main():
    A, B, C, D = map(int, sys.stdin.read().split())
    total = 0
    for r in range(4):
        ci = count_res(A, C - 1, r)
        if ci == 0:
            continue
        for s in range(4):
            cj = count_res(B, D - 1, s)
            if cj:
                total += ci * cj * value(r, s)
    print(total)


main()
