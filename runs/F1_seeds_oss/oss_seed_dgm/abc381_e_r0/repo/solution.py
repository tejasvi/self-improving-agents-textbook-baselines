# Write your solution here. Read from stdin, write to stdout.

import sys, bisect

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    S = next(it).decode()
    # prefix counts (1-indexed)
    pref1 = [0] * (N + 1)
    pref2 = [0] * (N + 1)
    slash_pos = []   # positions (1-indexed) where S[i-1] == '/'
    g_vals = []      # pref1[i-1] + pref2[i] for each slash position i
    for i, ch in enumerate(S, start=1):
        pref1[i] = pref1[i-1] + (ch == '1')
        pref2[i] = pref2[i-1] + (ch == '2')
        if ch == '/':
            slash_pos.append(i)
            g_vals.append(pref1[i-1] + pref2[i])
    out_lines = []
    for _ in range(Q):
        L = int(next(it))
        R = int(next(it))
        # find slashes inside [L,R]
        lo = bisect.bisect_left(slash_pos, L)
        hi = bisect.bisect_left(slash_pos, R + 1)
        if lo >= hi:
            out_lines.append('0')
            continue
        C = pref1[L-1] + pref2[R]
        # binary search for first index in [lo,hi) with g_vals[idx] >= C
        l = lo
        r = hi
        while l < r:
            m = (l + r) // 2
            if g_vals[m] >= C:
                r = m
            else:
                l = m + 1
        candidates = []
        if l < hi:
            candidates.append(slash_pos[l])
        if l - 1 >= lo:
            candidates.append(slash_pos[l - 1])
        best = 0
        for p in candidates:
            cnt1 = pref1[p-1] - pref1[L-1]
            cnt2 = pref2[R] - pref2[p]
            k = cnt1 if cnt1 < cnt2 else cnt2
            length = 2 * k + 1
            if length > best:
                best = length
        out_lines.append(str(best))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
