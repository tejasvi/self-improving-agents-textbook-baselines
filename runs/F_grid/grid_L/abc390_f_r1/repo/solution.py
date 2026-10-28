import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = data[1:1 + n]
    pos = {}
    for i in range(n):
        v = int(A[i])
        if v in pos:
            pos[v].append(i + 1)
        else:
            pos[v] = [i + 1]
    total = 0
    empty = []
    for v, P in pos.items():
        Q = pos.get(v - 1, empty)
        nq = len(Q)
        prev_p = 0
        for p in P:
            # last Q before p (or 0), first Q after p (or n+1)
            k = bisect_left(Q, p)
            lq = Q[k - 1] if k > 0 else 0
            rq = Q[k] if k < nq else n + 1
            lo = lq if lq > prev_p else prev_p
            total += (p - lo) * (rq - p)
            prev_p = p
    print(total)

main()
