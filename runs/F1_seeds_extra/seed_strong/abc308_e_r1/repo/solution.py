import sys

def mex3(x, y, z):
    s = {x, y, z}
    m = 0
    while m in s:
        m += 1
    return m

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    S = data[1 + n]
    # MEX[a][b][c] precomputed
    MX = [[[mex3(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]
    L = [0, 0, 0]
    R = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            R[A[i]] += 1
    total = 0
    for j in range(n):
        c = S[j]
        if c == 'X':
            R[A[j]] -= 1
        elif c == 'E':
            aj = A[j]
            for a in range(3):
                la = L[a]
                if la == 0:
                    continue
                row = MX[a][aj]
                for b in range(3):
                    rb = R[b]
                    if rb:
                        total += la * rb * row[b]
        elif c == 'M':
            L[A[j]] += 1
    print(total)

main()
