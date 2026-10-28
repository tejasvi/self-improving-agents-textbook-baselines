import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    P = [0] * (n + 1)
    for i in range(n):
        P[i + 1] = P[i] + A[i]
    # sparse table: sp[k][i] = max(A[i .. i+2^k-1])
    sp = [A]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        h = 1 << (k - 1)
        sp.append([max(x, y) for x, y in zip(prev, prev[h:])])
        k += 1
    K = len(sp)
    ks = list(range(K - 1, -1, -1))
    res = [0] * n
    for start in range(n):
        l = start
        r = start + 1  # half-open [l, r)
        s = A[start]
        while True:
            # extend left: find smallest l' such that all of A[l'..l-1] < s
            # binary descent: pos moves left while block of size 2^k ends at pos-1 and max < s
            if l == 0 or A[l - 1] >= s:
                nl = l
            else:
                pos = l
                for kk in ks:
                    w = 1 << kk
                    q = pos - w
                    if q >= 0 and sp[kk][q] < s:
                        pos = q
                nl = pos
            if r == n or A[r] >= s:
                nr = r
            else:
                pos = r
                for kk in ks:
                    w = 1 << kk
                    if pos + w <= n and sp[kk][pos] < s:
                        pos += w
                nr = pos
            if nl == l and nr == r:
                break
            s = P[nr] - P[nl]
            l = nl
            r = nr
        res[start] = P[r] - P[l]
    sys.stdout.write(" ".join(map(str, res)) + "\n")

main()
