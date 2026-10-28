import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); M = int(data[1])
    Ls = [int(data[2 + 2 * i]) for i in range(M)]
    Rs = [int(data[3 + 2 * i]) for i in range(M)]
    out_ops = [0] * M

    def emit(cost, ops):
        sys.stdout.write(str(cost) + "\n" + " ".join(map(str, ops)) + "\n")

    # Answer 1: a single interval [1, N]
    for i in range(M):
        if Ls[i] == 1 and Rs[i] == N:
            out_ops[i] = 1
            emit(1, out_ops)
            return

    # Answer 2: two disjoint intervals p (R_p < L_q)
    by_L = sorted(range(M), key=lambda i: Ls[i])
    by_R = sorted(range(M), key=lambda i: Rs[i])
    # min R over prefix in by_L order is not needed; check directly:
    # for each q, need p with R_p < L_q: min R over all intervals.
    minR_idx = by_R[0]
    for q in range(M):
        if Rs[minR_idx] < Ls[q]:
            out_ops[minR_idx] = 2
            out_ops[q] = 2
            emit(2, out_ops)
            return

    # Common point case. Prefix structures.
    sortedL = [Ls[i] for i in by_L]
    sortedR = [Rs[i] for i in by_R]

    # prefT[pos]: top-3 (R, idx) largest R among first pos intervals in by_L order
    prefT = [[]] * (M + 1)
    cur = []
    for pos in range(1, M + 1):
        i = by_L[pos - 1]
        cur = cur + [(Rs[i], i)]
        cur.sort(reverse=True)
        cur = cur[:3]
        prefT[pos] = cur
    # sufT[pos]: top-3 (smallest L, idx) among by_R[pos:]
    sufT = [[]] * (M + 1)
    cur = []
    for pos in range(M - 1, -1, -1):
        i = by_R[pos]
        cur = cur + [(Ls[i], i)]
        cur.sort()
        cur = cur[:3]
        sufT[pos] = cur
    # global orders
    minL_order = by_L  # ascending L
    maxR_order = by_R[::-1]  # descending R

    def evaluate(E, a, b):
        # returns (cov_cost, cover_indices) for target [a,b] excluding set E
        # 1-case: interval with L<=a and R>=b not in E
        pos = bisect_right(sortedL, a)
        for (r, idx) in prefT[pos]:
            if idx not in E:
                if r >= b:
                    return 1, [idx]
                break
        # 2-case
        r_idx = None
        for idx in minL_order:
            if idx not in E:
                r_idx = idx
                break
        s_idx = None
        for idx in maxR_order:
            if idx not in E:
                s_idx = idx
                break
        if r_idx is None or s_idx is None:
            return None, None
        if Ls[r_idx] <= a and Rs[s_idx] >= b:
            return 2, [r_idx, s_idx]
        return None, None

    best = None
    best_choice = None  # (E tuple, a, b)

    def consider(E, a, b):
        nonlocal best, best_choice
        c, cover = evaluate(E, a, b)
        if c is None:
            return
        total = len(E) + c
        if best is None or total < best:
            best = total
            best_choice = (E, cover)

    # empty S2: target [1, N]
    consider((), 1, N)
    # single S2
    for p in range(M):
        consider((p,), Ls[p], Rs[p])
    # pairs among top-K by L and top-K by R
    K = 4
    cand = set(by_L[-K:]) | set(by_R[:K])
    cand = list(cand)
    for x in range(len(cand)):
        for y in range(x + 1, len(cand)):
            p, q = cand[x], cand[y]
            a = max(Ls[p], Ls[q]); b = min(Rs[p], Rs[q])
            if a > b:
                continue
            consider((p, q), a, b)

    if best is None:
        print(-1)
        return
    E, cover = best_choice
    for e in E:
        out_ops[e] = 2
    for c in cover:
        out_ops[c] = 1
    emit(best, out_ops)


main()
