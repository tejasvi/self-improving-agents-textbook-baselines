import sys
import numpy as np


def block_contrib(v, s, pre):
    # for each value in v: sum over t in sorted block s of |v - t|
    m = len(s)
    k = np.searchsorted(s, v, side='left')
    return v * k - pre[k] + (pre[m] - pre[k]) - v * (m - k)


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = np.array(data[1:1 + n], dtype=np.int64)
    B = np.array(data[1 + n:1 + 2 * n], dtype=np.int64)
    k = int(data[1 + 2 * n])
    qs = np.array(data[2 + 2 * n:2 + 2 * n + 2 * k], dtype=np.int64).reshape(k, 2)

    S = 1500
    nb = n // S + 1  # block-count columns: b in [0, n//S]

    # PW[t][b] = sum_{j<t} sum_{i<b*S} |A_i - B_j|
    # PQ[t][c] = sum_{i<t} sum_{j<c*S} |A_i - B_j|
    PW = np.zeros((n + 1, nb), dtype=np.int64)
    PQ = np.zeros((n + 1, nb), dtype=np.int64)

    # PW build: cur over B indices, accumulate A blocks
    cur = np.zeros(n, dtype=np.int64)
    for b in range(nb):
        PW[1:, b] = np.cumsum(cur)
        lo, hi = b * S, min((b + 1) * S, n)
        if lo < hi:
            s = np.sort(A[lo:hi])
            pre = np.concatenate(([0], np.cumsum(s)))
            cur += block_contrib(B, s, pre)

    # PQ build: cur over A indices, accumulate B blocks
    cur = np.zeros(n, dtype=np.int64)
    for c in range(nb):
        PQ[1:, c] = np.cumsum(cur)
        lo, hi = c * S, min((c + 1) * S, n)
        if lo < hi:
            s = np.sort(B[lo:hi])
            pre = np.concatenate(([0], np.cumsum(s)))
            cur += block_contrib(A, s, pre)

    out = []
    for idx in range(k):
        x = int(qs[idx, 0])
        y = int(qs[idx, 1])
        bA = x // S
        cB = y // S
        ans = int(PW[cB * S, bA])
        ans += int(PQ[x, cB]) - int(PQ[bA * S, cB])
        ans += int(PW[y, bA]) - int(PW[cB * S, bA])
        I = A[bA * S:x]
        J = B[cB * S:y]
        if len(I) and len(J):
            s = np.sort(J)
            pre = np.concatenate(([0], np.cumsum(s)))
            ans += int(block_contrib(I, s, pre).sum())
        out.append(ans)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
