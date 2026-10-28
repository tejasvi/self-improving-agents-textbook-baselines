import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    t = data[1]
    m = len(t)
    strs = data[2:2 + n]

    # a_i: longest prefix of t that is a subsequence of S_i (greedy from left)
    # b_j: longest suffix of t that is a subsequence of S_j (greedy from right)
    a = [0] * n
    cnt = [0] * (m + 2)
    for idx in range(n):
        s = strs[idx]
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a[idx] = p
        q = m  # number of matched chars from the right: t[q:] matched
        for c in reversed(s):
            if q > 0 and t[q - 1] == c:
                q -= 1
        cnt[m - q] += 1

    # suf[v] = number of j with b_j >= v
    suf = [0] * (m + 2)
    running = 0
    for v in range(m, -1, -1):
        running += cnt[v]
        suf[v] = running

    total = 0
    for i in range(n):
        k = m - a[i]
        if k <= 0:
            total += n
        else:
            total += suf[k]
    print(total)


main()
