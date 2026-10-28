import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    t = data[1]
    strs = data[2:2 + n]
    m = len(t)

    # a_i: length of longest prefix of T that is a subsequence of S_i (greedy)
    # b_j: length of longest suffix of T that is a subsequence of S_j (greedy from end)
    cnt = [0] * (m + 2)
    a_list = [0] * n
    for i, s in enumerate(strs):
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a_list[i] = p

    rt = t[::-1]
    for j, s in enumerate(strs):
        q = 0
        for c in reversed(s):
            if q < m and rt[q] == c:
                q += 1
        cnt[q] += 1

    # suffix sums: suf[k] = number of j with b_j >= k
    suf = [0] * (m + 2)
    acc = 0
    for k in range(m, -1, -1):
        acc += cnt[k]
        suf[k] = acc

    ans = 0
    for a in a_list:
        need = m - a
        if need < 0:
            need = 0
        ans += suf[need]
    print(ans)


main()
