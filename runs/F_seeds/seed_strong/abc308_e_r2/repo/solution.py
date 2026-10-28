import sys

def mex3(a, b, c):
    s = {a, b, c}
    m = 0
    while m in s:
        m += 1
    return m

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    S = data[1 + n]
    W = [[[mex3(a, b, c) for c in range(3)] for a in range(3)] for b in range(3)]
    pre = [0, 0, 0]
    suf = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            suf[A[i]] += 1
    total = 0
    for j in range(n):
        ch = S[j]
        if ch == 'X':
            suf[A[j]] -= 1
        elif ch == 'M':
            pre[A[j]] += 1
        else:  # 'E'
            if pre[0] + pre[1] + pre[2] and suf[0] + suf[1] + suf[2]:
                w = W[A[j]]
                s = 0
                for a in range(3):
                    if pre[a]:
                        wa = w[a]
                        for c in range(3):
                            s += pre[a] * suf[c] * wa[c]
                total += s
    print(total)

main()
