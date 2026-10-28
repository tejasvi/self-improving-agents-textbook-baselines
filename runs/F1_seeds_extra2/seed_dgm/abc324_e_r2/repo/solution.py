import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    t = data[1]
    strs = data[2:2 + n]
    m = len(t)

    # a_i: longest prefix of T that is a subsequence of S_i (greedy)
    # b_j: longest suffix of T that is a subsequence of S_j (greedy from the right)
    cnt = [0] * (m + 2)
    a_vals = []
    for s in strs:
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a_vals.append(p)

        q = m - 1
        for c in reversed(s):
            if q >= 0 and t[q] == c:
                q -= 1
        cnt[m - 1 - q] += 1

    # suf[v] = number of j with b_j >= v
    suf = [0] * (m + 2)
    running = 0
    for v in range(m, -1, -1):
        running += cnt[v]
        suf[v] = running

    ans = 0
    for a in a_vals:
        ans += suf[m - a]
    print(ans)


main()
