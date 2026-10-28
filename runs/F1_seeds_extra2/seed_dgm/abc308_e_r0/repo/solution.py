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

    L = [0, 0, 0]  # M's at indices < j, by A value
    R = [0, 0, 0]  # X's at indices > j, by A value
    for j in range(n):
        if S[j] == 'X':
            R[A[j]] += 1
    total = 0
    for j in range(n):
        c = S[j]
        if c == 'X':
            R[A[j]] -= 1
        elif c == 'E':
            e = A[j]
            for a in range(3):
                la = L[a]
                if la == 0:
                    continue
                row = MEX[a][e]
                for b in range(3):
                    rb = R[b]
                    if rb:
                        total += la * rb * row[b]
        elif c == 'M':
            L[A[j]] += 1
    print(total)

main()
