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

    # MEX[a][e][b] precomputed
    MEX = [[[mex3(a, e, b) for b in range(3)] for e in range(3)] for a in range(3)]

    leftM = [0, 0, 0]
    rightX = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            rightX[A[i]] += 1
    total = 0
    for j in range(n):
        c = S[j]
        if c == 'X':
            rightX[A[j]] -= 1
        elif c == 'E':
            e = A[j]
            for a in range(3):
                la = leftM[a]
                if la == 0:
                    continue
                row = MEX[a][e]
                for b in range(3):
                    rb = rightX[b]
                    if rb:
                        total += la * rb * row[b]
        elif c == 'M':
            leftM[A[j]] += 1
    print(total)

main()
