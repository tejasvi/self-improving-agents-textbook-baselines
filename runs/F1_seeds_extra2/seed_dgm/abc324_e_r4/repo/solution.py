import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = data[1]
    strs = data[2:2 + n]
    m = len(t)
    rt = t[::-1]

    # For each S_i: p_i = longest prefix of T that is a subsequence of S_i (greedy).
    # For each S_j: s_j = longest suffix of T that is a subsequence of S_j (greedy from right).
    # Pair (i, j) valid iff p_i + s_j >= m.
    p_vals = []
    cnt = [0] * (m + 2)
    for s in strs:
        k = 0
        for c in s:
            if k < m and c == t[k]:
                k += 1
                if k == m:
                    break
        p_vals.append(k)

        k2 = 0
        for c in reversed(s):
            if k2 < m and c == rt[k2]:
                k2 += 1
                if k2 == m:
                    break
        cnt[k2] += 1

    # suf[x] = number of j with s_j >= x
    suf = [0] * (m + 2)
    running = 0
    for x in range(m, -1, -1):
        running += cnt[x]
        suf[x] = running

    ans = 0
    for p in p_vals:
        need = m - p
        if need < 0:
            need = 0
        ans += suf[need]
    print(ans)


main()
