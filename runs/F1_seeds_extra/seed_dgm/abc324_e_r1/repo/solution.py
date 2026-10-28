import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = data[1].decode()
    strs = [s.decode() for s in data[2:2 + n]]
    m = len(t)

    # a_i: longest prefix of T that is a subsequence of S_i (greedy from left)
    # b_j: longest suffix of T that is a subsequence of S_j (greedy from right)
    a = [0] * n
    b = [0] * n
    for idx, s in enumerate(strs):
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a[idx] = p
        q = 0
        for c in reversed(s):
            if q < m and t[m - 1 - q] == c:
                q += 1
        b[idx] = q

    # cnt[v] = number of j with b_j == v ; suf[v] = number with b_j >= v
    cnt = [0] * (m + 2)
    for v in b:
        cnt[v] += 1
    suf = [0] * (m + 2)
    running = 0
    for v in range(m, -1, -1):
        running += cnt[v]
        suf[v] = running

    ans = 0
    for i in range(n):
        need = m - a[i]
        ans += suf[need]
    print(ans)


main()
