from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # Check if total sum is at least target
        total_sum = sum(nums)
        if total_sum < target:
            return -1
        
        # Count occurrences of each power of 2
        # Use a dictionary with power as key: 2^i -> count
        power_count = {}
        for num in nums:
            if num not in power_count:
                power_count[num] = 0
            power_count[num] += 1
        
        operations = 0
        current_power = 1
        
        # Process from smallest to largest power
        while target > 0:
            if current_power in power_count and power_count[current_power] > 0:
                # We have this power available
                if current_power <= target:
                    # Use it towards the target
                    power_count[current_power] -= 1
                    target -= current_power
                else:
                    # We don't need this power for target, keep it for combining
                    pass
            else:
                # We don't have this power, need to split a larger one
                power_count[current_power] = 0
                
                # Find the next available power larger than current_power
                next_power = current_power * 2
                while next_power not in power_count or power_count[next_power] == 0:
                    next_power *= 2
                
                # Split down from next_power to current_power
                while next_power > current_power:
                    operations += 1
                    power_count[next_power] -= 1
                    next_power //= 2
                    power_count[next_power] = power_count.get(next_power, 0) + 2
                
                # Now we have current_power available, use it
                power_count[current_power] -= 1
                target -= current_power
            
            current_power *= 2
        
        return operations
