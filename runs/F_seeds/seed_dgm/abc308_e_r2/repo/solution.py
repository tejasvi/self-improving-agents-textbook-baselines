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

    # mex table indexed [a][e][c]
    MX = [[[mex3(a, e, c) for c in range(3)] for e in range(3)] for a in range(3)]

    pm = [0, 0, 0]  # counts of M-values at indices before current
    sx = [0, 0, 0]  # counts of X-values at indices after current
    for i in range(n):
        if S[i] == 'X':
            sx[A[i]] += 1
    # Now sx counts all X; we need to remove as we pass. Handle by decrementing
    # when we reach an X index (before processing any E at later index).
    total = 0
    for i in range(n):
        ch = S[i]
        if ch == 'X':
            sx[A[i]] -= 1
        elif ch == 'E':
            e = A[i]
            for a in range(3):
                pa = pm[a]
                if pa == 0:
                    continue
                row = MX[a][e]
                for c in range(3):
                    if sx[c]:
                        total += pa * sx[c] * row[c]
        elif ch == 'M':
            pm[A[i]] += 1
    print(total)


main()
