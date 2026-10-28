import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    T = data[1].decode()
    M = len(T)
    S = [x.decode() for x in data[2:2 + n]]
    Trev = T[::-1]
    a = [0] * n
    b = [0] * n
    for i, s in enumerate(S):
        p = 0
        for c in s:
            if p < M and T[p] == c:
                p += 1
                if p == M:
                    break
        a[i] = p
        q = 0
        for c in reversed(s):
            if q < M and Trev[q] == c:
                q += 1
                if q == M:
                    break
        b[i] = q
    cnt = [0] * (M + 2)
    for v in b:
        cnt[v] += 1
    # suf[v] = number of j with b_j >= v
    suf = [0] * (M + 2)
    run = 0
    for v in range(M, -1, -1):
        run += cnt[v]
        suf[v] = run
    total = 0
    for x in a:
        need = M - x
        if need <= 0:
            total += n
        else:
            total += suf[need]
    print(total)

main()
