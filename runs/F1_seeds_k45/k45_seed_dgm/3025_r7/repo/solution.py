from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # First check if total sum is enough
        total_sum = sum(nums)
        if total_sum < target:
            return -1
        
        # Count frequency of each power of 2
        # Use a dictionary to count powers
        freq = {}
        for num in nums:
            freq[num] = freq.get(num, 0) + 1
        
        operations = 0
        
        # Process from smallest to largest power
        # We need to greedily use powers to reach the target
        power = 1
        remaining = target
        
        while remaining > 0:
            if remaining & 1:  # We need this power
                if power in freq and freq[power] > 0:
                    # Use one occurrence of this power
                    freq[power] -= 1
                    remaining -= power
                else:
                    # We don't have this power, need to break down a larger power
                    # Find the next larger power we have
                    p = power * 2
                    found = False
                    while p <= total_sum:
                        if p in freq and freq[p] > 0:
                            # Break down from this power to the one we need
                            # This requires operations: we need to repeatedly split
                            # p -> p/2, p/2 and continue until we get to power
                            found = True
                            bit_diff = 0
                            temp_p = p
                            while temp_p > power:
                                temp_p //= 2
                                bit_diff += 1
                            
                            # Remove the larger power and add broken down pieces
                            freq[p] -= 1
                            # Add the pieces back
                            temp_p = p // 2
                            for _ in range(bit_diff):
                                freq[temp_p] = freq.get(temp_p, 0) + 1
                                if temp_p == power:
                                    break
                                temp_p //= 2
                            
                            operations += bit_diff
                            break
                        p *= 2
                    
                    if not found:
                        return -1  # Can't reach target
                    
                    if power in freq and freq[power] > 0:
                        freq[power] -= 1
                        remaining -= power
            else:
                # We don't need this power, but we can combine pairs into next power
                if power in freq:
                    pairs = freq[power] // 2
                    if pairs > 0:
                        freq[power * 2] = freq.get(power * 2, 0) + pairs
                    freq[power] = freq[power] % 2
            
            power *= 2
        
        return operations
