# Write your solution here. Read from stdin, write to stdout.
import sys

def mex_of_three(a, b, c):
    # values are 0,1,2
    # return smallest non-negative integer not in {a,b,c}
    present = [False] * 4
    present[a] = True
    present[b] = True
    present[c] = True
    for i in range(4):
        if not present[i]:
            return i
    return 4  # unreachable

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    S = list(next(it).strip())
    # precompute suffix counts of X positions
    suffix = [0, 0, 0]
    for i in range(N):
        if S[i] == 'X':
            suffix[A[i]] += 1
    # prefix counts for M positions
    prefix = [0, 0, 0]
    # precompute mex table
    mex_table = [[[0]*3 for _ in range(3)] for __ in range(3)]
    for a in range(3):
        for b in range(3):
            for c in range(3):
                mex_table[a][b][c] = mex_of_three(a, b, c)
    ans = 0
    for idx in range(N):
        # move current X out of suffix (since we need k>idx)
        if S[idx] == 'X':
            suffix[A[idx]] -= 1
        if S[idx] == 'E':
            b = A[idx]
            for a in range(3):
                cnt_a = prefix[a]
                if cnt_a == 0:
                    continue
                for c in range(3):
                    cnt_c = suffix[c]
                    if cnt_c == 0:
                        continue
                    ans += cnt_a * cnt_c * mex_table[a][b][c]
        if S[idx] == 'M':
            prefix[A[idx]] += 1
    print(ans)

if __name__ == "__main__":
    solve()
