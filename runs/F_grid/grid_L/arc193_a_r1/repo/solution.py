import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    W = [int(x) for x in data[pos:pos + n]]; pos += n
    L = [0] * n
    R = [0] * n
    for i in range(n):
        L[i] = int(data[pos]); R[i] = int(data[pos + 1]); pos += 2
    M = 2 * n + 3
    INF = float('inf')
    # PB[p]: min W over vertices x with R_x <= p  ("x entirely left of p")
    # SA[p]: min W over vertices y with L_y >= p ("y entirely right of p")
    PB = [INF] * (M + 1)
    SA = [INF] * (M + 2)
    for i in range(n):
        if W[i] < PB[R[i]]:
            PB[R[i]] = W[i]
        if W[i] < SA[L[i]]:
            SA[L[i]] = W[i]
    for p in range(1, M + 1):
        if PB[p - 1] < PB[p]:
            PB[p] = PB[p - 1]
    for p in range(M, -1, -1):
        if SA[p + 1] < SA[p]:
            SA[p] = SA[p + 1]

    q = int(data[pos]); pos += 1
    out = []
    for _ in range(q):
        s = int(data[pos]) - 1; t = int(data[pos + 1]) - 1; pos += 2
        ls, rs, lt, rt = L[s], R[s], L[t], R[t]
        if rs < lt or rt < ls:
            out.append(W[s] + W[t])
            continue
        # intervals intersect: paths of length <= 3 suffice
        best = PB[min(ls, lt) - 1]
        c = SA[max(rs, rt) + 1]
        if c < best:
            best = c
        c = PB[ls - 1] + SA[rt + 1]
        if c < best:
            best = c
        c = PB[lt - 1] + SA[rs + 1]
        if c < best:
            best = c
        if best == INF:
            out.append(-1)
        else:
            out.append(int(best) + W[s] + W[t])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
