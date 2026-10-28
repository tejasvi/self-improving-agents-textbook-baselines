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

    # total X counts to the right of each position
    cntX = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            cntX[A[i]] += 1
    cntM = [0, 0, 0]
    total = 0
    # table[a][b][c]
    MX = [[[mex(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]
    for j in range(n):
        s = S[j]
        if s == 'X':
            cntX[A[j]] -= 1
        elif s == 'M':
            cntM[A[j]] += 1
        else:
            b = A[j]
            for a in range(3):
                la = cntM[a]
                if la == 0:
                    continue
                row = MX[a][b]
                for c in range(3):
                    total += la * cntX[c] * row[c]
    print(total)

main()
