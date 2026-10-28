import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    T = data[1].decode()
    S = [x.decode() for x in data[2:2 + n]]
    m = len(T)
    a = [0] * n
    b = [0] * n
    for i, s in enumerate(S):
        p = 0
        for c in s:
            if p < m and T[p] == c:
                p += 1
                if p == m:
                    break
        a[i] = p
        q = m  # matched suffix length
        for c in reversed(s):
            if q > 0 and T[q - 1] == c:
                q -= 1
                if q == 0:
                    break
        b[i] = m - q
    cnt = [0] * (m + 2)
    for v in b:
        cnt[v] += 1
    # suf[v] = number of j with b_j >= v
    suf = [0] * (m + 2)
    run = 0
    for v in range(m, -1, -1):
        run += cnt[v]
        suf[v] = run
    ans = 0
    for x in a:
        need = m - x
        if need <= 0:
            ans += n
        else:
            ans += suf[need]
    print(ans)

main()
