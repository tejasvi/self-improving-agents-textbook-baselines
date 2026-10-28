import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = data[1]
    strs = data[2:2 + n]
    m = len(t)

    # a_i: longest prefix of T that is a subsequence of S_i
    # b_j: longest suffix of T that is a subsequence of S_j
    a = [0] * n
    cnt = [0] * (m + 2)
    for i in range(n):
        s = strs[i]
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
                if p == m:
                    break
        a[i] = p

        q = m
        for c in reversed(s):
            if q > 0 and t[q - 1] == c:
                q -= 1
                if q == 0:
                    break
        cnt[m - q] += 1

    # suf[k] = number of j with b_j >= k
    suf = [0] * (m + 2)
    running = 0
    for k in range(m, -1, -1):
        running += cnt[k]
        suf[k] = running

    total = 0
    for i in range(n):
        need = m - a[i]
        if need <= 0:
            total += n
        else:
            total += suf[need]
    print(total)


main()
