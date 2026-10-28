from typing import List

class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        nums.sort()
        n = len(nums)
        result = 0
        
        # For each element as the minimum
        for i in range(n):
            min_val = nums[i]
            
            # Contribution when this element is minimum and is alone
            result = (result + min_val * (min_val ** 2)) % MOD
            
            # Contribution when this element is minimum paired with others
            power_of_2 = 1  # 2^0 for the element itself being included
            
            for j in range(i + 1, n):
                max_val = nums[j]
                # For each element nums[j] as potential maximum,
                # it can pair with any subset of elements between i+1 and j (inclusive)
                # that doesn't include a smaller element (which would be the new minimum)
                # So we have 2^(j-i-1) groups where nums[j] is max and nums[i] is min
                
                contribution = (max_val * max_val) % MOD
                contribution = (contribution * min_val) % MOD
                contribution = (contribution * power_of_2) % MOD
                result = (result + contribution) % MOD
                
                power_of_2 = (power_of_2 * 2) % MOD
        
        return result
