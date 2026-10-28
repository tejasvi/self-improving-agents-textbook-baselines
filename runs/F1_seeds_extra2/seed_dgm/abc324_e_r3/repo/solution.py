import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    t = data[1]
    m = len(t)
    strs = data[2:2 + n]

    # a[i]: longest prefix of T that is a subsequence of S_i (greedy from left)
    a = [0] * n
    # b[j]: longest suffix of T that is a subsequence of S_j (greedy from right)
    b = [0] * n
    rt = t[::-1]
    for idx, s in enumerate(strs):
        p = 0
        for c in s:
            if p < m and c == t[p]:
                p += 1
        a[idx] = p
        q = 0
        for c in reversed(s):
            if q < m and c == rt[q]:
                q += 1
        b[idx] = q

    # cnt_ge[k] = number of j with b[j] >= k, for k in 0..m+1
    cnt = [0] * (m + 2)
    for v in b:
        cnt[v] += 1
    for k in range(m - 1, -1, -1):
        cnt[k] += cnt[k + 1]

    ans = 0
    for v in a:
        need = m - v
        if need < 0:
            need = 0
        ans += cnt[need]
    print(ans)


main()
