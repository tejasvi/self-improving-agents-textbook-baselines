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
    MEX = [[[mex3(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]
    cntM = [0, 0, 0]
    cntX = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            cntX[A[i]] += 1
    total = 0
    for j in range(n):
        ch = S[j]
        if ch == 'X':
            cntX[A[j]] -= 1
        elif ch == 'E':
            b = A[j]
            for a in range(3):
                ca = cntM[a]
                if ca:
                    row = MEX[a][b]
                    for c in range(3):
                        cc = cntX[c]
                        if cc:
                            total += ca * cc * row[c]
        elif ch == 'M':
            cntM[A[j]] += 1
    print(total)

main()
