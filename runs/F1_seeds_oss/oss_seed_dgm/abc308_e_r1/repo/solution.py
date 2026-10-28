# Solution for MEX problem
import sys

def solve():
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
    # suffix counts of X positions by value
    suffix = [0, 0, 0]
    for i in range(N):
        if S[i] == 'X':
            suffix[A[i]] += 1
    prefix = [0, 0, 0]
    ans = 0
    for i in range(N):
        ch = S[i]
        # current position should not be counted in suffix for future indices
        if ch == 'X':
            suffix[A[i]] -= 1
        if ch == 'E':
            aj = A[i]
            for a in range(3):
                ca = prefix[a]
                if ca == 0:
                    continue
                for c in range(3):
                    cc = suffix[c]
                    if cc == 0:
                        continue
                    ans += ca * cc * mex[a][aj][c]
        if ch == 'M':
            prefix[A[i]] += 1
    print(ans)

if __name__ == "__main__":
    solve()
