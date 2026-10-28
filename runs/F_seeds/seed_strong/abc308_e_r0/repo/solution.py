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
    A = [int(v) for v in data[1:1 + n]]
    S = data[1 + n]
    MEX = [[[mex3(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]
    sx = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            sx[A[i]] += 1
    pm = [0, 0, 0]
    total = 0
    for j in range(n):
        ch = S[j]
        if ch == 'X':
            sx[A[j]] -= 1
        elif ch == 'E':
            b = A[j]
            for a in range(3):
                if pm[a]:
                    row = MEX[a][b]
                    for c in range(3):
                        if sx[c]:
                            total += pm[a] * sx[c] * row[c]
        else:
            if ch == 'M':
                pm[A[j]] += 1
    print(total)


main()
