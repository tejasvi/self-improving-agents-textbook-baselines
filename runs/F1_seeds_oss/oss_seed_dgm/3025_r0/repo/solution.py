from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # Count frequency of each power of two
        MAX_BIT = 31  # enough for numbers up to 2^30 and target up to 2^31-1
        freq = [0] * MAX_BIT
        for num in nums:
            # Determine the bit position (since num is a power of two)
            bit = num.bit_length() - 1  # because 2^k has bit_length k+1
            freq[bit] += 1

        ops = 0
        carry = 0  # surplus pieces from lower bits that can be paired upward
        for i in range(MAX_BIT):
            # Does target require a 2^i piece?
            need = (target >> i) & 1
            # Total pieces of size 2^i we have at this moment
            available = freq[i] + carry
            if available >= need:
                # Use what we need, surplus passes upward (pairable)
                surplus = available - need
            else:
                # Need to create more by splitting a larger piece
                j = i + 1
                while j < MAX_BIT and freq[j] == 0:
                    j += 1
                if j == MAX_BIT:
                    # No larger piece to split – impossible
                    return -1
                # Perform one split chain from level j down to i
                ops += (j - i)
                # Use one piece of size 2^j
                freq[j] -= 1
                # After splitting, it becomes 2^{j-i} pieces of size 2^i
                added = 1 << (j - i)
                available = freq[i] + carry + added
                # Now we must have enough (by construction)
                surplus = available - need
            # Surplus pieces can form pairs to become pieces of next higher bit
            carry = surplus // 2
        return ops
