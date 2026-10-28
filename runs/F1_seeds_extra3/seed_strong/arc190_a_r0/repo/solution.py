import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    L = [int(x) for x in data[2:2 + 2 * m:2]]
    R = [int(x) for x in data[3:3 + 2 * m:2]]

    def out(k, ops):
        sys.stdout.write(str(k) + "\n" + " ".join(map(str, ops)) + "\n")

    # Cost 1: a single interval equal to [1, N] (operation 1).
    for i in range(m):
        if L[i] == 1 and R[i] == n:
            ops = [0] * m
            ops[i] = 1
            out(1, ops)
            return

    # Cost 2, case A: two type-1 intervals covering [1, N].
    a = -1  # among L == 1, max R
    b = -1  # among R == N, min L
    for i in range(m):
        if L[i] == 1 and (a < 0 or R[i] > R[a]):
            a = i
        if R[i] == n and (b < 0 or L[i] < L[b]):
            b = i
    if a >= 0 and b >= 0 and L[b] <= R[a] + 1:
        ops = [0] * m
        ops[a] = 1
        ops[b] = 1
        out(2, ops)
        return

    # Cost 2, case B: two type-2 intervals that are disjoint.
    imin = min(range(m), key=lambda i: R[i])
    for i in range(m):
        if L[i] > R[imin]:
            ops = [0] * m
            ops[imin] = 2
            ops[i] = 2
            out(2, ops)
            return

    # Cost 2, case C: type-1 interval s containing type-2 interval t.
    order = sorted(range(m), key=lambda i: (L[i], -R[i]))
    best_r = -1
    best_idx = -1
    for t in order:
        if best_idx >= 0 and best_r >= R[t]:
            ops = [0] * m
            ops[best_idx] = 1
            ops[t] = 2
            out(2, ops)
            return
        if R[t] > best_r:
            best_r = R[t]
            best_idx = t

    sys.stdout.write("-1\n")


main()
