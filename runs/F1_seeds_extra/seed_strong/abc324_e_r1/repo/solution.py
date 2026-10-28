import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    t = data[1]
    m = len(t)
    strs = data[2:2 + n]
    rt = t[::-1]

    a = [0] * n
    b = [0] * n
    for idx in range(n):
        s = strs[idx]
        p = 0
        for c in s:
            if p < m and t[p] == c:
                p += 1
        a[idx] = p
        q = 0
        for c in reversed(s):
            if q < m and rt[q] == c:
                q += 1
        b[idx] = q

    # cnt over b values, then suffix sums: suf[k] = #j with b_j >= k
    cnt = [0] * (m + 2)
    for v in b:
        cnt[v] += 1
    suf = [0] * (m + 2)
    run = 0
    for k in range(m, -1, -1):
        run += cnt[k]
        suf[k] = run

    total = 0
    for v in a:
        need = m - v
        if need <= 0:
            total += n
        else:
            total += suf[need]
    print(total)

main()
