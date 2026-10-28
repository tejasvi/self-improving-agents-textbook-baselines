from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # Check if total sum is at least target
        total_sum = sum(nums)
        if total_sum < target:
            return -1
        
        # If total sum equals target and we already have the exact sum, no operations needed
        if total_sum == target:
            return 0
        
        # Count frequency of each power of 2
        # Use a dictionary where key is the bit position and value is the count
        count = {}
        for num in nums:
            bit_pos = 0
            temp = num
            while temp > 1:
                temp //= 2
                bit_pos += 1
            count[bit_pos] = count.get(bit_pos, 0) + 1
        
        operations = 0
        bit_pos = 0
        
        # Process the target bit by bit from least significant to most significant
        while target > 0:
            power_of_2 = 1 << bit_pos
            
            if target & power_of_2:
                # We need this bit in the target
                if count.get(bit_pos, 0) > 0:
                    # We have this power, use it
                    count[bit_pos] -= 1
                else:
                    # We don't have this power, need to find a larger one and split
                    next_bit = bit_pos + 1
                    while count.get(next_bit, 0) == 0:
                        next_bit += 1
                    
                    # Split from next_bit down to bit_pos
                    count[next_bit] -= 1
                    for b in range(next_bit - 1, bit_pos - 1, -1):
                        count[b] = count.get(b, 0) + 1
                        operations += 1
                    
                    # Now use this bit
                    count[bit_pos] -= 1
            
            # Carry over: combine pairs of current bit into the next bit
            if count.get(bit_pos, 0) > 0:
                count[bit_pos + 1] = count.get(bit_pos + 1, 0) + count[bit_pos] // 2
            
            target >>= 1
            bit_pos += 1
        
        return operations
