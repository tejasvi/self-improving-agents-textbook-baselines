import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    S = data[1 + n]

    # mex table for values in {0,1,2}
    mex = [[[0] * 3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                m = 0
                while m in (a, b, c):
                    m += 1
                mex[a][b][c] = m

    pm = [0, 0, 0]   # counts of M values before current position
    sx = [0, 0, 0]   # counts of X values after current position
    for i in range(n):
        if S[i] == 'X':
            sx[A[i]] += 1
    ans = 0
    for j in range(n):
        ch = S[j]
        v = A[j]
        if ch == 'X':
            sx[v] -= 1
        elif ch == 'E':
            for a in range(3):
                if pm[a] == 0:
                    continue
                for c in range(3):
                    if sx[c]:
                        ans += pm[a] * sx[c] * mex[a][v][c]
        elif ch == 'M':
            pm[v] += 1
    print(ans)


main()
