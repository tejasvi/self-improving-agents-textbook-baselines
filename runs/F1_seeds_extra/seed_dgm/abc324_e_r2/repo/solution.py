import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = data[1]
    m = len(t)
    strs = data[2:2 + n]

    # a_i: longest prefix of T obtained greedily as a subsequence of S_i
    a = [0] * n
    # b_j: longest suffix of T obtained greedily (from the right) as a subsequence of S_j
    b = [0] * n
    for idx, s in enumerate(strs):
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a[idx] = p

        q = m
        for c in reversed(s):
            if q > 0 and t[q - 1] == c:
                q -= 1
        b[idx] = m - q

    # cnt[k] = number of j with b_j == k ; suf[k] = number of j with b_j >= k
    cnt = [0] * (m + 2)
    for v in b:
        cnt[v] += 1
    suf = [0] * (m + 2)
    acc = 0
    for k in range(m, -1, -1):
        acc += cnt[k]
        suf[k] = acc

    ans = 0
    for x in a:
        need = m - x  # need b_j >= need
        ans += suf[need]
    print(ans)


main()
