import sys
from itertools import accumulate
from operator import add


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    N = int(data[2])
    holes = {}
    idx = 3
    for _ in range(N):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        holes.setdefault(a, []).append(b)

    # x(i,j) = largest holeless square with top-left (i,j).
    # x(i,j) = 0 if holed, else min(x(i+1,j), x(i+1,j+1), x(i,j+1)) + 1.
    # With y_j = x_j + j:  y_j = min(C_j, y_{j+1}), C_j = min(P_j, P_{j+1}) + j + 1,
    # and C_j = j for holed cells (so y_j = j). Solved by a suffix-min scan.
    J = list(range(1, W + 1))
    J1 = [j + 1 for j in J]
    half = W * (W + 1) // 2
    P = [0] * (W + 2)  # P[j] = x(i+1, j), P[W+1] = 0
    total = 0
    for i in range(H, 0, -1):
        C = list(map(add, map(min, P[1:W + 1], P[2:W + 2]), J1))
        row_holes = holes.get(i)
        if row_holes:
            for b in row_holes:
                C[b - 1] = b
        rev = [W + 1]
        rev.extend(reversed(C))
        acc = list(accumulate(rev, min))
        Y = acc[:0:-1]  # y_1..y_W
        sy = sum(Y)
        total += sy - half
        newP = [0] * (W + 2)
        newP[1:W + 1] = [y - j for y, j in zip(Y, J)]
        P = newP
    print(total)


main()
