from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # Check if total sum is at least target
        if sum(nums) < target:
            return -1
        
        # Count frequency of each power of 2
        # We'll use a dictionary where key is the power (exponent) and value is count
        from collections import defaultdict
        power_count = defaultdict(int)
        
        for num in nums:
            # Find the power of 2
            power = 0
            temp = num
            while temp > 1:
                temp //= 2
                power += 1
            power_count[power] += 1
        
        operations = 0
        current_sum = 0
        
        # Process from smallest power to largest
        # We need to greedily pick powers to form the target sum
        power = 0
        
        while current_sum < target:
            # If we have this power available, use it
            if power_count[power] > 0:
                power_count[power] -= 1
                current_sum += (1 << power)  # Add 2^power to sum
            else:
                # We don't have 2^power, we need to split a larger power
                # Find the next larger power that we have
                next_power = power + 1
                while power_count[next_power] == 0:
                    next_power += 1
                
                # Split all powers from next_power down to power
                power_count[next_power] -= 1
                for p in range(next_power, power, -1):
                    power_count[p - 1] += 2
                    operations += 1
                
                # Now use one of the 2^power
                power_count[power] -= 1
                current_sum += (1 << power)
            
            power += 1
        
        return operations
