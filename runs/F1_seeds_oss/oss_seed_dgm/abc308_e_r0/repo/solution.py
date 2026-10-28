# Write your solution here. Read from stdin, write to stdout.

import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    S = next(it).strip()
    # Precompute mex for all triples of values 0..2
    mex = [[[0]*3 for _ in range(3)] for __ in range(3)]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                s = {a, b, c}
                m = 0
                while m in s:
                    m += 1
                mex[a][b][c] = m
    # suffix counts of X for each value
    suffixX = [[0,0,0] for _ in range(N+1)]
    for i in range(N-1, -1, -1):
        suffixX[i][0] = suffixX[i+1][0]
        suffixX[i][1] = suffixX[i+1][1]
        suffixX[i][2] = suffixX[i+1][2]
        if S[i] == 'X':
            v = A[i]
            suffixX[i][v] += 1
    prefixM = [0,0,0]
    ans = 0
    for j in range(N):
        if S[j] == 'E':
            b = A[j]
            # counts of M before j
            for a in range(3):
                cntM = prefixM[a]
                if cntM == 0:
                    continue
                for c in range(3):
                    cntX = suffixX[j+1][c]
                    if cntX == 0:
                        continue
                    ans += mex[a][b][c] * cntM * cntX
        # after processing position j, update prefix if it's M
        if S[j] == 'M':
            prefixM[A[j]] += 1
    print(ans)

if __name__ == "__main__":
    main()
