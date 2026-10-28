import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    A = np.array(data[pos:pos + n], dtype=np.int64); pos += n
    B = np.array(data[pos:pos + n], dtype=np.int64); pos += n
    k = int(data[pos]); pos += 1
    qs = np.array(data[pos:pos + 2 * k], dtype=np.int64).reshape(k, 2)
    X = qs[:, 0].copy()
    Y = qs[:, 1].copy()

    S = max(1, int(round(n ** 0.5)))

    # Sorted-order helpers: prefix sorted arrays via boolean masks.
    ordA = np.argsort(A, kind='stable')
    sortedA_vals = A[ordA]
    sortedA_idx = ordA
    ordB = np.argsort(B, kind='stable')
    sortedB_vals = B[ordB]
    sortedB_idx = ordB

    ans = np.zeros(k, dtype=np.int64)

    P = X // S  # block index for x
    Q = Y // S  # block index for y

    # Part 1 & 3: loop over p (x-block), uses rows i < pS.
    order_p = np.argsort(P, kind='stable')
    Ps = P[order_p]
    # group boundaries
    uniq_p, starts_p = np.unique(Ps, return_index=True)
    ends_p = list(starts_p[1:]) + [k]
    for up, st, en in zip(uniq_p.tolist(), starts_p.tolist(), ends_p):
        qidx = order_p[st:en]
        m = up * S
        # sorted prefix of A[:m]
        if m > 0:
            sv = sortedA_vals[sortedA_idx < m]
            PS = np.zeros(m + 1, dtype=np.int64)
            np.cumsum(sv, out=PS[1:])
            # G[j] = sum_{i<m} |A_i - B_j|
            cnt = np.searchsorted(sv, B, side='left')
            v = B
            G = v * cnt - PS[cnt] + (PS[m] - PS[cnt]) - v * (m - cnt)
        else:
            G = np.zeros(n, dtype=np.int64)
        Gc = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(G, out=Gc[1:])
        xq = X[qidx]
        yq = Y[qidx]
        qb = (yq // S) * S
        ans[qidx] += Gc[qb] + (Gc[yq] - Gc[qb])

    # Part 2: loop over q (y-block), rows i in [pS, x), cols j < qS.
    order_q = np.argsort(Q, kind='stable')
    Qs = Q[order_q]
    uniq_q, starts_q = np.unique(Qs, return_index=True)
    ends_q = list(starts_q[1:]) + [k]
    for uq, st, en in zip(uniq_q.tolist(), starts_q.tolist(), ends_q):
        qidx = order_q[st:en]
        m = uq * S
        if m > 0:
            sb = sortedB_vals[sortedB_idx < m]
            PB = np.zeros(m + 1, dtype=np.int64)
            np.cumsum(sb, out=PB[1:])
            cnt = np.searchsorted(sb, A, side='left')
            v = A
            H = v * cnt - PB[cnt] + (PB[m] - PB[cnt]) - v * (m - cnt)
        else:
            H = np.zeros(n, dtype=np.int64)
        Hc = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(H, out=Hc[1:])
        xq = X[qidx]
        pb = (xq // S) * S
        ans[qidx] += Hc[xq] - Hc[pb]

    # Part 4: corner, rows [pS, x), cols [qS, y).
    for t in range(k):
        x = int(X[t]); y = int(Y[t])
        r0 = (x // S) * S
        c0 = (y // S) * S
        if x > r0 and y > c0:
            a = A[r0:x]
            sb = np.sort(B[c0:y])
            m = sb.shape[0]
            PB = np.zeros(m + 1, dtype=np.int64)
            np.cumsum(sb, out=PB[1:])
            cnt = np.searchsorted(sb, a, side='left')
            ans[t] += int((a * cnt - PB[cnt]).sum() + ((PB[m] - PB[cnt]) - a * (m - cnt)).sum())

    sys.stdout.write('\n'.join(map(str, ans.tolist())) + '\n')


main()
