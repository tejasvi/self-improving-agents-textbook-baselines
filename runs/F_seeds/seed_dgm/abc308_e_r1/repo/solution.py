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

    # MEX[b][a][c]
    MEX = [[[mex3(a, b, c) for c in range(3)] for a in range(3)] for b in range(3)]

    L = [0, 0, 0]
    R = [0, 0, 0]
    for j in range(n):
        if S[j] == 'X':
            R[A[j]] += 1
    total = 0
    for j in range(n):
        ch = S[j]
        if ch == 'X':
            R[A[j]] -= 1
        elif ch == 'E':
            b = A[j]
            M = MEX[b]
            s = 0
            for a in range(3):
                la = L[a]
                if la:
                    row = M[a]
                    for c in range(3):
                        s += la * R[c] * row[c]
            total += s
        elif ch == 'M':
            L[A[j]] += 1
    print(total)


main()
