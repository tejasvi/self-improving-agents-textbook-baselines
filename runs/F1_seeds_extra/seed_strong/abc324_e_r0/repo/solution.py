import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    T = data[1]
    m = len(T)
    S = data[2:2 + n]
    a = [0] * n
    b = [0] * n
    for i, s in enumerate(S):
        p = 0
        for ch in s:
            if p < m and T[p] == ch:
                p += 1
        a[i] = p
        q = 0
        for ch in reversed(s):
            if q < m and T[m - 1 - q] == ch:
                q += 1
        b[i] = q
    cnt = [0] * (m + 2)
    for v in b:
        cnt[v] += 1
    # ge[k] = number of j with b_j >= k
    ge = [0] * (m + 2)
    acc = 0
    for k in range(m, -1, -1):
        acc += cnt[k]
        ge[k] = acc
    ans = 0
    for v in a:
        ans += ge[m - v]
    print(ans)

main()
