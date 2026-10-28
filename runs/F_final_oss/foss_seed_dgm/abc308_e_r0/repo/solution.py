# Write your solution here. Read from stdin, write to stdout.
import sys

def mex3(x, y, z):
    # Compute mex of three numbers each in {0,1,2}
    # Use bitmask or set
    present = {x, y, z}
    for m in range(4):
        if m not in present:
            return m
    return 4  # never reached

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    S = next(it).strip()

    # suffix counts of X positions for each value
    suffix = [[0, 0, 0] for _ in range(N + 1)]
    for i in range(N - 1, -1, -1):
        suffix[i][0] = suffix[i + 1][0]
        suffix[i][1] = suffix[i + 1][1]
        suffix[i][2] = suffix[i + 1][2]
        if S[i] == 'X':
            v = A[i]
            suffix[i][v] += 1

    prefix = [0, 0, 0]
    ans = 0
    for j in range(N):
        if S[j] == 'E':
            a_j = A[j]
            after = suffix[j + 1]
            # iterate over possible values of M and X
            for a in range(3):
                cntM = prefix[a]
                if cntM == 0:
                    continue
                for c in range(3):
                    cntX = after[c]
                    if cntX == 0:
                        continue
                    ans += cntM * cntX * mex3(a, a_j, c)
        if S[j] == 'M':
            prefix[A[j]] += 1
    print(ans)

if __name__ == "__main__":
    main()
