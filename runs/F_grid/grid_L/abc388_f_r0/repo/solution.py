import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); A = int(data[2]); B = int(data[3])
    intervals = []
    idx = 4
    for _ in range(M):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        intervals.append((L, R))
    intervals.sort()

    # A bad block of length >= B makes it impossible to cross.
    for L, R in intervals:
        if R - L + 1 >= B:
            print("No")
            return

    # State S: bit k set <=> we can be at position (pos - k), k in [0, B-1].
    full = (1 << B) - 1
    mask = full ^ ((1 << (A - 1)) - 1)  # bits A-1 .. B-1

    def step_free(S):
        new0 = 1 if (S & mask) else 0
        return (((S << 1) & full) | new0)

    def step_bad(S):
        return (S << 1) & full

    def apply_table(table, S):
        res = 0
        j = 0
        while S:
            if S & 1:
                res |= table[j]
            S >>= 1
            j += 1
        return res

    # g[p][j] = step_free^(2^p) applied to the single bit j (linear over OR)
    LOG = 42  # 2^41 > 1e12
    g = [[step_free(1 << j) for j in range(B)]]
    for _ in range(1, LOG):
        prev = g[-1]
        g.append([apply_table(prev, prev[j]) for j in range(B)])

    def advance_free(S, d):
        p = 0
        while d:
            if d & 1:
                S = apply_table(g[p], S)
                if S == 0:
                    return 0
            d >>= 1
            p += 1
        return S

    S = 1
    pos = 1
    for L, R in intervals:
        d = (L - 1) - pos
        if d > 0:
            S = advance_free(S, d)
            if S == 0:
                print("No")
                return
        pos = L - 1
        for _ in range(R - L + 1):
            S = step_bad(S)
            pos += 1
        if S == 0:
            print("No")
            return
    d = N - pos
    if d > 0:
        S = advance_free(S, d)
    print("Yes" if (S & 1) else "No")


main()
