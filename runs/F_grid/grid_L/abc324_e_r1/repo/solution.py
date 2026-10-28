import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = data[1]
    strs = data[2:2 + n]
    m = len(t)

    # a_i: longest prefix of T that is a subsequence of S_i (greedy from left)
    # b_j: longest suffix of T that is a subsequence of S_j (greedy from right)
    a = [0] * n
    b = [0] * n
    for idx in range(n):
        s = strs[idx]
        p = 0
        for c in s:
            if p < m and c == t[p]:
                p += 1
        a[idx] = p

        q = m
        for c in reversed(s):
            if q > 0 and c == t[q - 1]:
                q -= 1
        b[idx] = m - q

    # cnt_suffix[k] = number of j with b_j >= k
    cnt = [0] * (m + 2)
    for v in b:
        cnt[v] += 1
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
