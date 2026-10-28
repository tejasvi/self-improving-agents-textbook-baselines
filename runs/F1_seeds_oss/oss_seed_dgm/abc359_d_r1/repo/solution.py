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
    max_mask = 1 << (K - 1) if K > 1 else 1
    dp = [0] * max_mask
    dp[0] = 1
    mask_limit = (1 << (K - 1)) - 1 if K > 1 else 0
    for pos, ch in enumerate(S):
        new_dp = [0] * max_mask
        allowed = []
        if ch == 'A':
            allowed = [0]
        elif ch == 'B':
            allowed = [1]
        else:  # '?'
            allowed = [0, 1]
        for mask in range(max_mask):
            val = dp[mask]
            if val == 0:
                continue
            for c in allowed:
                # check palindrome constraint if we have a full window of length K
                if K <= pos + 1:
                    # we have at least K characters after adding c
                    # extract the oldest character among the previous K-1 bits
                    oldest = (mask >> (K - 2)) & 1
                    # build the K-length window
                    full = [0] * K
                    full[0] = oldest
                    # fill middle bits from mask (excluding the oldest bit)
                    for i in range(1, K - 1):
                        bit_index = K - 2 - i
                        full[i] = (mask >> bit_index) & 1
                    full[K - 1] = c
                    # check if this window is a palindrome
                    is_pal = True
                    for i in range(K // 2):
                        if full[i] != full[K - 1 - i]:
                            is_pal = False
                            break
                    if is_pal:
                        continue  # this choice creates a forbidden palindrome
                # update mask
                new_mask = ((mask << 1) | c) & mask_limit if K > 1 else 0
                new_dp[new_mask] = (new_dp[new_mask] + val) % MOD
        dp = new_dp
    ans = sum(dp) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
