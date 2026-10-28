import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    S = data[1 + n]

    def mex(a, b, c):
        s = {a, b, c}
        m = 0
        while m in s:
            m += 1
        return m

    # MEX[a][b][c]
    MEX = [[[mex(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]

    preM = [0, 0, 0]
    sufX = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            sufX[A[i]] += 1
    total = 0
    for j in range(n):
        ch = S[j]
        a_j = A[j]
        if ch == 'M':
            preM[a_j] += 1
        elif ch == 'X':
            sufX[a_j] -= 1
        else:  # 'E'
            for a in range(3):
                pa = preM[a]
                if pa == 0:
                    continue
                row = MEX[a][a_j]
                for c in range(3):
                    total += row[c] * pa * sufX[c]
    print(total)


main()
