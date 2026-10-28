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

    MEX = [[[mex3(x, e, y) for y in range(3)] for e in range(3)] for x in range(3)]

    right = [0, 0, 0]  # counts of X by value, to the right of current position
    for i in range(n):
        if S[i] == 'X':
            right[A[i]] += 1

    left = [0, 0, 0]  # counts of M by value, to the left of current position
    total = 0
    for j in range(n):
        c = S[j]
        if c == 'M':
            left[A[j]] += 1
        elif c == 'X':
            right[A[j]] -= 1
        else:  # 'E'
            e = A[j]
            for x in range(3):
                lx = left[x]
                if lx == 0:
                    continue
                row = MEX[x][e]
                for y in range(3):
                    ry = right[y]
                    if ry:
                        total += row[y] * lx * ry
    print(total)


main()
