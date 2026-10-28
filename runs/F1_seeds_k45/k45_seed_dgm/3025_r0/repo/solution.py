from typing import List
from collections import defaultdict

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # First check if total sum is enough
        total_sum = sum(nums)
        if total_sum < target:
            return -1
        
        # Create a frequency map for powers of 2
        # Key: power (so 2^power), Value: count of that power
        power_count = defaultdict(int)
        
        for num in nums:
            power = 0
            temp = num
            while temp > 1:
                temp //= 2
                power += 1
            power_count[power] += 1
        
        operations = 0
        current_power = 0
        
        # Process bit by bit from LSB to MSB
        while target > 0:
            # Check if current bit of target is set
            if target & 1:
                # We need a power of 2^current_power
                if power_count[current_power] > 0:
                    # We have it, use it
                    power_count[current_power] -= 1
                else:
                    # We don't have it, need to break down a larger power
                    # Find the next power we have
                    next_power = current_power + 1
                    while next_power in power_count and power_count[next_power] == 0:
                        next_power += 1
                    
                    # If we can't find any power >= current_power, something went wrong
                    if next_power not in power_count and power_count[next_power] == 0:
                        # Need to check if we can reach this from available powers
                        pass
                    
                    # Break down from next_power to current_power
                    while next_power > current_power:
                        power_count[next_power] -= 1
                        power_count[next_power - 1] += 2
                        operations += 1
                        next_power -= 1
                    
                    # Now use one of current_power
                    power_count[current_power] -= 1
            
            # Combine pairs of current_power into current_power + 1
            # (this is free and helps us have larger powers for future needs)
            power_count[current_power + 1] += power_count[current_power] // 2
            
            # Move to next bit
            target >>= 1
            current_power += 1
        
        return operations
