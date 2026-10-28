import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    # e[p] = h(p) - p, where h(p) = first index j with A[j] >= 2*A[p]
    e = [bisect_left(A, 2 * A[p]) - p for p in range(n)]
    # sparse table: sp[j][i] = max(e[i .. i+2^j-1])
    sp = [e]
    j = 1
    while (1 << j) <= n:
        prev = sp[-1]
        half = 1 << (j - 1)
        cur = [max(prev[i], prev[i + half]) for i in range(n - (1 << j) + 1)]
        sp.append(cur)
        j += 1
    LOG = len(sp)
    out = []
    idx = 2 + n
    NEG = -(1 << 60)
    for _ in range(q):
        L = int(data[idx]) - 1
        R = int(data[idx + 1]) - 1
        idx += 2
        ln = R - L + 1
        half_len = ln // 2
        pos = L
        K = 0
        cm = NEG
        for lv in range(LOG - 1, -1, -1):
            step = 1 << lv
            nk = K + step
            if nk > half_len:
                continue
            # need pos + step - 1 <= n-1 (guaranteed since nk <= half_len and pos+nk-1 <= R)
            m = sp[lv][pos]
            if m < cm:
                m = cm
            if m + nk <= ln:
                K = nk
                cm = m
                pos += step
        out.append(K)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
