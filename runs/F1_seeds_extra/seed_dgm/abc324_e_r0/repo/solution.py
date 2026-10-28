import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = data[1]
    m = len(t)
    strs = data[2:2 + n]

    a_vals = []
    b_cnt = [0] * (m + 2)
    for s in strs:
        # longest prefix of t that is a subsequence of s (greedy)
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a_vals.append(p)
        # longest suffix of t that is a subsequence of s (greedy from right)
        q = m - 1
        for c in reversed(s):
            if q >= 0 and t[q] == c:
                q -= 1
        b_cnt[m - 1 - q] += 1

    # suf[v] = number of j with b_j >= v
    suf = [0] * (m + 2)
    for v in range(m, -1, -1):
        suf[v] = suf[v + 1] + b_cnt[v]

    ans = 0
    for a in a_vals:
        need = m - a
        if need <= 0:
            ans += n
        else:
            ans += suf[need]
    print(ans)


main()
