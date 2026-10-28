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

    MX = [[[mex(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]

    # Right counts of X by value
    R = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            R[A[i]] += 1
    L = [0, 0, 0]
    total = 0
    for j in range(n):
        ch = S[j]
        if ch == 'X':
            R[A[j]] -= 1
        elif ch == 'M':
            L[A[j]] += 1
        else:  # 'E'
            b = A[j]
            s = 0
            for a in range(3):
                la = L[a]
                if la == 0:
                    continue
                row = MX[a][b]
                for c in range(3):
                    s += la * R[c] * row[c]
            total += s
    print(total)


main()
