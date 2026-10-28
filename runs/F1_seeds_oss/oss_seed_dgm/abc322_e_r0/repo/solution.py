# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    P = int(next(it))
    C = []
    A = []
    for _ in range(N):
        c = int(next(it))
        C.append(c)
        a = [int(next(it)) for _ in range(K)]
        A.append(a)
    base = P + 1
    total_states = base ** K
    INF = 10**18
    dp = [INF] * total_states
    dp[0] = 0  # all zeros

    # precompute powers for encoding/decoding
    pow_base = [base ** i for i in range(K)]

    def decode(idx):
        # returns list of length K with each coordinate
        coords = []
        for i in range(K):
            coords.append(idx % base)
            idx //= base
        return coords

    def encode(coords):
        idx = 0
        mult = 1
        for v in coords:
            idx += v * mult
            mult *= base
        return idx

    for i in range(N):
        a = A[i]
        cost = C[i]
        new_dp = dp[:]  # copy current dp
        for idx in range(total_states):
            cur_cost = dp[idx]
            if cur_cost == INF:
                continue
            # compute new state after taking plan i
            coords = []
            tmp = idx
            for _ in range(K):
                coord = tmp % base
                tmp //= base
                # add contribution, cap at P
                new_coord = coord + a[_]
                if new_coord > P:
                    new_coord = P
                coords.append(new_coord)
            new_idx = 0
            mult = 1
            for v in coords:
                new_idx += v * mult
                mult *= base
            # update
            if new_dp[new_idx] > cur_cost + cost:
                new_dp[new_idx] = cur_cost + cost
        dp = new_dp

    target_idx = total_states - 1  # all coordinates are P (since base=P+1, highest index)
    ans = dp[target_idx]
    if ans >= INF:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
