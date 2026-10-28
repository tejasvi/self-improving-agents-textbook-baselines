import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    S = data[1 + n]

    def mex(*vals):
        s = set(vals)
        m = 0
        while m in s:
            m += 1
        return m

    MEX = [[[mex(a, b, c) for c in range(3)] for b in range(3)] for a in range(3)]

    # Right-side counts of X by value (positions after current index)
    cntX = [0, 0, 0]
    for i in range(n):
        if S[i] == 'X':
            cntX[A[i]] += 1
    cntM = [0, 0, 0]
    total = 0
    for j in range(n):
        c = S[j]
        if c == 'X':
            cntX[A[j]] -= 1
        elif c == 'M':
            cntM[A[j]] += 1
        else:  # 'E'
            a_val = A[j]
            for i_val in range(3):
                li = cntM[i_val]
                if li == 0:
                    continue
                row = MEX[i_val][a_val]
                for k_val in range(3):
                    rk = cntX[k_val]
                    if rk:
                        total += li * rk * row[k_val]
    print(total)

main()
