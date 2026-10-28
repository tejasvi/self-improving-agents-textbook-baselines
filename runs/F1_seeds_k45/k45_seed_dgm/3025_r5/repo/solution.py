from typing import List
from collections import defaultdict

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # Check if the total sum is at least the target
        total_sum = sum(nums)
        if total_sum < target:
            return -1
        
        # Count the frequency of each power of 2
        power_count = defaultdict(int)
        for num in nums:
            power_count[num] += 1
        
        operations = 0
        current_power = 1
        
        while target > 0:
            # If we need the current power and have it available
            if current_power in power_count and power_count[current_power] > 0:
                # Use one of the current power for the target (if needed)
                if target >= current_power:
                    target -= current_power
                    power_count[current_power] -= 1
                # Move to the next power
                current_power *= 2
            # If we don't have the current power, we need to get it from a larger power
            else:
                # Find the smallest power larger than current_power that we have
                next_power = current_power * 2
                found = False
                
                while next_power not in power_count or power_count[next_power] == 0:
                    next_power *= 2
                    # Safety check to avoid infinite loop
                    if next_power > total_sum:
                        return -1
                
                # Split from next_power down to current_power
                while next_power > current_power:
                    power_count[next_power] -= 1
                    next_power //= 2
                    power_count[next_power] += 2
                    operations += 1
                
                # Now we have current_power available
                # Don't move to next power yet, process current_power
        
        return operations
