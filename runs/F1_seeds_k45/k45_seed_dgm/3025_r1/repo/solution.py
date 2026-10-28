from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # First check if total sum is less than target
        total_sum = sum(nums)
        if total_sum < target:
            return -1
        
        # Count frequency of each power of 2
        # key: power of 2, value: count
        power_count = {}
        for num in nums:
            if num not in power_count:
                power_count[num] = 0
            power_count[num] += 1
        
        operations = 0
        current_power = 1  # Start with 2^0 = 1
        
        while target > 0:
            if current_power not in power_count or power_count[current_power] == 0:
                # We don't have this power, need to find a larger one and split it
                larger_power = current_power * 2
                found = False
                
                while larger_power <= total_sum:
                    if larger_power in power_count and power_count[larger_power] > 0:
                        # Found a larger power, split it down to current_power
                        power_count[larger_power] -= 1
                        
                        # Split from larger_power down to current_power
                        temp_power = larger_power
                        while temp_power > current_power:
                            temp_power //= 2
                            if temp_power not in power_count:
                                power_count[temp_power] = 0
                            power_count[temp_power] += 2
                            operations += 1
                        
                        # Now we have current_power available
                        power_count[current_power] -= 1
                        target -= current_power
                        found = True
                        break
                    
                    larger_power *= 2
                
                if not found:
                    return -1
            else:
                # We have this power, use it
                power_count[current_power] -= 1
                target -= current_power
            
            current_power *= 2
        
        return operations
