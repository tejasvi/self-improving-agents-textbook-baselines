# Write your solution here. Read from stdin, write to stdout.
import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    S = data[2].strip()
    # Mapping: A -> 0, B -> 1
    max_mask = 1 << (K - 1) if K > 1 else 1
    dp = [0] * max_mask
    dp[0] = 1  # no previous characters yet
    # Pre‑compute whether a window becomes a palindrome
    # is_pal[mask][c] = True if the length‑K substring formed by the previous K‑1 bits (mask) and the new char c is a palindrome
    is_pal = [[False, False] for _ in range(max_mask)]
    if K == 1:
        # Not possible per constraints (K >= 2), but keep for completeness
        for mask in range(max_mask):
            is_pal[mask][0] = is_pal[mask][1] = True
    else:
        for mask in range(max_mask):
            # extract bits of mask: bit (K-2) is the oldest, bit 0 is the newest among the stored K-1 chars
            for c in (0, 1):
                seq = []
                for i in range(K - 2, -1, -1):
                    seq.append((mask >> i) & 1)
                seq.append(c)
                # check palindrome
                pal = True
                for i in range(K // 2):
                    if seq[i] != seq[K - 1 - i]:
                        pal = False
                        break
                is_pal[mask][c] = pal
    mask_all = (1 << (K - 1)) - 1 if K > 1 else 0
    # DP over positions
    for idx, ch in enumerate(S):
        ndp = [0] * max_mask
        for mask in range(max_mask):
            cur = dp[mask]
            if cur == 0:
                continue
            # try both possible characters
            for c in (0, 1):
                # respect fixed characters
                if ch != '?' and ((c == 0 and ch != 'A') or (c == 1 and ch != 'B')):
                    continue
                # if we already have a full window, reject if it would be a palindrome
                if idx + 1 >= K and is_pal[mask][c]:
                    continue
                new_mask = ((mask << 1) | c) & mask_all if K > 1 else 0
                ndp[new_mask] = (ndp[new_mask] + cur) % MOD
        dp = ndp
    ans = sum(dp) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
