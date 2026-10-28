import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    S = data[1 + n]

    def mex3(a, b, c):
        s = {a, b, c}
        m = 0
        while m in s:
            m += 1
        return m

    MEX = [[[mex3(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]

    L = [0, 0, 0]
    R = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            R[A[i]] += 1
    total = 0
    for p in range(n):
        ch = S[p]
        if ch == 'X':
            R[A[p]] -= 1
        elif ch == 'E':
            b = A[p]
            for a in range(3):
                la = L[a]
                if la == 0:
                    continue
                row = MEX[a][b]
                for c in range(3):
                    total += la * R[c] * row[c]
        else:  # 'M'
            L[A[p]] += 1
    print(total)


main()
