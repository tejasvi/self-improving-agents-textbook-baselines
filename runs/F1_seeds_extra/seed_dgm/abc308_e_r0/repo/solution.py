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
    # table[a][e][b] = mex(a, e, b)
    table = [[[mex3(a, e, b) for b in range(3)] for e in range(3)] for a in range(3)]
    mc = [0, 0, 0]  # count of M's before current position, by value
    xc = [0, 0, 0]  # count of X's after current position, by value
    for i in range(n):
        if S[i] == 'X':
            xc[A[i]] += 1
    total = 0
    for p in range(n):
        ch = S[p]
        if ch == 'M':
            mc[A[p]] += 1
        elif ch == 'X':
            xc[A[p]] -= 1
        else:  # 'E'
            e = A[p]
            s = 0
            for a in range(3):
                if mc[a] == 0:
                    continue
                row = table[a][e]
                inner = 0
                for b in range(3):
                    inner += row[b] * xc[b]
                s += mc[a] * inner
            total += s
    print(total)

main()
