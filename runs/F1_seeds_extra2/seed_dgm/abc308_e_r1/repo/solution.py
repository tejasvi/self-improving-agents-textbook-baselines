import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    S = data[1 + n]

    def mex3(a, b, c):
        s = {a, b, c}
        v = 0
        while v in s:
            v += 1
        return v

    # table[a][b][c]
    table = [[[mex3(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]

    preM = [0, 0, 0]
    sufX = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            sufX[A[i]] += 1

    ans = 0
    for j in range(n):
        ch = S[j]
        if ch == 'E':
            b = A[j]
            for a in range(3):
                pa = preM[a]
                if pa == 0:
                    continue
                for c in range(3):
                    sc = sufX[c]
                    if sc:
                        ans += pa * sc * table[a][b][c]
        elif ch == 'M':
            preM[A[j]] += 1
        elif ch == 'X':
            sufX[A[j]] -= 1
    print(ans)


main()
