from typing import List
from collections import defaultdict

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # First check if total sum is at least target
        total_sum = sum(nums)
        if total_sum < target:
            return -1
        
        # Count frequency of each power of 2
        # Key is the bit position (power k for 2^k)
        power_count = defaultdict(int)
        
        for num in nums:
            # Get the power of 2: num = 2^k
            # Find k such that 2^k = num
            power = 0
            temp = num
            while temp > 1:
                temp //= 2
                power += 1
            power_count[power] += 1
        
        operations = 0
        power = 0
        
        # Process each bit of target from least significant
        while target > 0:
            if target & 1:  # This bit is needed
                if power_count[power] > 0:
                    # We have this power, use it
                    power_count[power] -= 1
                else:
                    # We don't have this power, need to get it by splitting larger powers
                    next_power = power + 1
                    
                    # Find next power that we have
                    while power_count[next_power] == 0:
                        next_power += 1
                        # Safety check: if next_power gets too large, we have a problem
                        if next_power > 60:  # 2^60 is larger than 2^31
                            return -1
                    
                    # Split down from next_power to power
                    while next_power > power:
                        power_count[next_power] -= 1
                        power_count[next_power - 1] += 2
                        operations += 1
                        next_power -= 1
                    
                    # Now use one of power
                    power_count[power] -= 1
            else:
                # This bit is not needed
                # Combine two of current power into next power
                if power_count[power] >= 2:
                    power_count[power] -= 2
                    power_count[power + 1] += 1
            
            target >>= 1
            power += 1
        
        return operations
