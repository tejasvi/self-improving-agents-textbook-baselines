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
    # DP over last K-1 bits (states). For K=1 would be trivial but K>=2 per constraints.
    max_mask = 1 << (K - 1)  # number of possible histories of length K-1
    dp = [0] * max_mask
    dp[0] = 1  # empty prefix has no history
    mask_limit = max_mask - 1
    for i, ch in enumerate(S):
        # Determine which characters can be placed here: 0 for 'A', 1 for 'B'
        if ch == '?':
            possibilities = [0, 1]
        elif ch == 'A':
            possibilities = [0]
        else:  # ch == 'B'
            possibilities = [1]
        new_dp = [0] * max_mask
        for mask in range(max_mask):
            cur = dp[mask]
            if cur == 0:
                continue
            for c in possibilities:
                # If we have already K-1 previous characters, we can form a window of length K
                if i >= K - 1:
                    # Build the full window of K characters: the first K-1 come from mask, last is c
                    # mask stores previous K-1 chars with the most recent at the least‑significant bit
                    # i.e., for j = 0..K-2 (oldest to newest): bit = (mask >> (K-2-j)) & 1
                    is_pal = True
                    for j in range(K // 2):
                        # left character at position j in the window
                        if j == K - 1 - j:  # middle character for odd K, not needed
                            continue
                        # Determine left char
                        if j < K - 1:
                            left = (mask >> (K - 2 - j)) & 1
                        else:
                            left = c  # this case never occurs because j < K//2 <= K-1
                        # Determine right character at position K-1-j
                        rpos = K - 1 - j
                        if rpos == K - 1:
                            right = c
                        else:
                            right = (mask >> (K - 2 - rpos)) & 1
                        if left != right:
                            is_pal = False
                            break
                    if is_pal:
                        # This window would be a palindrome, so this placement is invalid
                        continue
                # Update mask: shift left, add current character, keep only K-1 bits
                new_mask = ((mask << 1) | c) & mask_limit
                new_dp[new_mask] = (new_dp[new_mask] + cur) % MOD
        dp = new_dp
    ans = sum(dp) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
