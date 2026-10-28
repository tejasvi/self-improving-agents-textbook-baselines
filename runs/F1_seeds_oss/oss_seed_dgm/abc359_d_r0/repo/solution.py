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
    # Convert characters to possible bits (0 for A, 1 for B)
    possible = []
    for ch in S:
        if ch == 'A':
            possible.append([0])
        elif ch == 'B':
            possible.append([1])
        else:  # '?'
            possible.append([0, 1])
    # We keep the last K-1 bits in a mask (LSB = most recent character)
    max_mask = 1 << (K - 1)  # K >= 2 by constraints
    dp = [0] * max_mask
    dp[0] = 1
    mask_limit = max_mask - 1
    half = K // 2
    for i in range(N):
        ndp = [0] * max_mask
        for mask in range(max_mask):
            cur = dp[mask]
            if cur == 0:
                continue
            for c in possible[i]:
                # If we already have at least K characters, check whether the substring of length K ending here is a palindrome.
                if K <= i + 1:
                    is_palindrome = True
                    for d in range(half):
                        left_off = K - 1 - d   # distance from current position to the left character
                        right_off = d           # distance to the right character
                        # character at left_off
                        if left_off == 0:
                            left_char = c
                        else:
                            left_char = (mask >> (left_off - 1)) & 1
                        # character at right_off
                        if right_off == 0:
                            right_char = c
                        else:
                            right_char = (mask >> (right_off - 1)) & 1
                        if left_char != right_char:
                            is_palindrome = False
                            break
                    if is_palindrome:
                        # This would create a forbidden palindrome of length K.
                        continue
                new_mask = ((mask << 1) | c) & mask_limit
                ndp[new_mask] = (ndp[new_mask] + cur) % MOD
        dp = ndp
    ans = sum(dp) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
