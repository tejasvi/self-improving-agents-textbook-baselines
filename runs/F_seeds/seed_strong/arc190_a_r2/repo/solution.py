import sys


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    M = int(data[1])
    L = [0] * M
    R = [0] * M
    for i in range(M):
        L[i] = int(data[2 + 2 * i])
        R[i] = int(data[3 + 2 * i])

    def out(cost, ops):
        sys.stdout.write(str(cost) + "\n" + " ".join(map(str, ops)) + "\n")

    # Cost 1: a single op1 interval equal to [1, N].
    for i in range(M):
        if L[i] == 1 and R[i] == N:
            ops = [0] * M
            ops[i] = 1
            out(1, ops)
            return

    # Cost 2, type A: two op1 intervals i (L=1) and j (R=N) with L_j <= R_i + 1.
    left = [i for i in range(M) if L[i] == 1]     # want max R
    right = [j for j in range(M) if R[j] == N]    # want min L
    left.sort(key=lambda i: -R[i])
    right.sort(key=lambda j: L[j])
    for i in left[:2]:
        for j in right[:2]:
            if i != j and L[j] <= R[i] + 1:
                ops = [0] * M
                ops[i] = 1
                ops[j] = 1
                out(2, ops)
                return

    # Cost 2, type B: op2 on i, op1 on j with [L_j, R_j] containing [L_i, R_i].
    # Sort by L; for each distinct L value, keep top-2 R (with indices) over prefix.
    order = sorted(range(M), key=lambda k: L[k])
    # prefix top-2 by R, evaluated at each position in order (after including all with same L)
    best_at = {}  # index -> (top1 idx, top2 idx) for prefix including all with L <= L[index]
    t1 = -1
    t2 = -1
    p = 0
    while p < M:
        q = p
        v = L[order[p]]
        while q < M and L[order[q]] == v:
            k = order[q]
            if t1 == -1 or R[k] > R[t1]:
                t2 = t1
                t1 = k
            elif t2 == -1 or R[k] > R[t2]:
                t2 = k
            q += 1
        for r in range(p, q):
            best_at[order[r]] = (t1, t2)
        p = q
    for i in range(M):
        a, b = best_at[i]
        j = a if a != i else b
        if j != -1 and R[j] >= R[i]:
            ops = [0] * M
            ops[i] = 2
            ops[j] = 1
            out(2, ops)
            return

    # Cost 2, type C: two disjoint op2 intervals i, j with R_i < L_j.
    byR = sorted(range(M), key=lambda k: R[k])
    a0 = byR[0]
    a1 = byR[1] if M > 1 else -1
    for j in range(M):
        i = a0 if a0 != j else a1
        if i != -1 and R[i] < L[j]:
            ops = [0] * M
            ops[i] = 2
            ops[j] = 2
            out(2, ops)
            return

    print(-1)


main()
