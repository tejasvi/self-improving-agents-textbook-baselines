import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    T = data[1]
    M = len(T)
    S = data[2:2 + n]
    a_vals = []
    cnt = [0] * (M + 2)
    for s in S:
        p = 0
        for c in s:
            if p < M and T[p] == c:
                p += 1
        a_vals.append(p)
        q = M
        for c in reversed(s):
            if q > 0 and T[q - 1] == c:
                q -= 1
        cnt[M - q] += 1
    # suf[k] = number of j with b_j >= k
    suf = [0] * (M + 2)
    running = 0
    for k in range(M, -1, -1):
        running += cnt[k]
        suf[k] = running
    total = 0
    for a in a_vals:
        need = M - a
        if need <= 0:
            total += n
        else:
            total += suf[need]
    print(total)

main()
