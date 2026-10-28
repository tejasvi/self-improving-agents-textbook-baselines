# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    import sys
    input_data = sys.stdin.read().strip().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    W = int(next(it))
    items = []
    for _ in range(N):
        w = int(next(it))
        v = int(next(it))
        items.append((w, v))
    INF_NEG = -10**18
    dp = [INF_NEG] * (W + 1)
    dp[0] = 0
    for w, v in items:
        dp2 = dp[:]  # copy, representing not taking any of this type
        # process each residue modulo w
        for r in range(w):
            # collect indices for this residue
            idxs = []
            t = 0
            pos = r
            while pos <= W:
                idxs.append(pos)
                t += 1
                pos += w
            m_len = len(idxs)
            if m_len == 0:
                continue
            # f[t] = dp at weight idxs[t]
            f = [dp[idx] for idx in idxs]
            # convex hull deque of lines (slope, intercept)
            deque = []  # each element is (m, b)
            # helper to evaluate line at x = t
            def value(line, x):
                m, b = line
                return m * x + b
            # helper to determine whether middle line is unnecessary
            def is_bad(a, b, c):
                # a, b, c are (m, b) with increasing slopes
                # return True if b is unnecessary
                m1, b1 = a
                m2, b2 = b
                m3, b3 = c
                # intersection(a,b) >= intersection(b,c)
                # (b2 - b1)/(m1 - m2) >= (b3 - b2)/(m2 - m3)
                # cross multiply (note denominators are negative because slopes increase)
                return (b2 - b1) * (m2 - m3) >= (b3 - b2) * (m1 - m2)
            # iterate over t
            for t_idx, pos in enumerate(idxs):
                # query best line for current t_idx
                while len(deque) >= 2 and value(deque[0], t_idx) <= value(deque[1], t_idx):
                    deque.pop(0)
                if deque:
                    best = value(deque[0], t_idx)
                    g = -t_idx * t_idx + t_idx * v + best
                    if g > dp2[pos]:
                        dp2[pos] = g
                # add line for j = t_idx
                if f[t_idx] > INF_NEG // 2:
                    m_line = 2 * t_idx
                    b_line = f[t_idx] - t_idx * t_idx - t_idx * v
                    new_line = (m_line, b_line)
                    while len(deque) >= 2 and is_bad(deque[-2], deque[-1], new_line):
                        deque.pop()
                    deque.append(new_line)
        dp = dp2
    ans = max(dp)
    print(ans)

if __name__ == "__main__":
    solve()
