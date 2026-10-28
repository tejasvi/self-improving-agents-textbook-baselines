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

    # Precompute mex table
    MEX = [[[mex3(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]

    preM = [0, 0, 0]
    sufX = [0, 0, 0]
    for k in range(n):
        if S[k] == 'X':
            sufX[A[k]] += 1

    total = 0
    for j in range(n):
        sj = S[j]
        if sj == 'X':
            sufX[A[j]] -= 1
            continue
        if sj == 'E':
            aj = A[j]
            for a in range(3):
                pa = preM[a]
                if pa == 0:
                    continue
                row = MEX[a][aj]
                for c in range(3):
                    sc = sufX[c]
                    if sc:
                        total += row[c] * pa * sc
        elif sj == 'M':
            preM[A[j]] += 1
    print(total)


main()
