from typing import List
import math

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        """
        Find the k-th alternating permutation in lexicographical order.
        An alternating permutation has no two adjacent elements that are both odd or both even.
        """
        # Separate odd and even numbers
        odds = list(range(1, n + 1, 2))  # [1, 3, 5, ...]
        evens = list(range(2, n + 1, 2))  # [2, 4, 6, ...]
        
        num_odds = len(odds)
        num_evens = len(evens)
        
        # Calculate total number of alternating permutations
        # An alternating permutation must alternate between odd and even
        # We can start with odd or even
        # If starting with odd: odd, even, odd, even, ... (needs num_odds >= num_evens)
        # If starting with even: even, odd, even, odd, ... (needs num_evens >= num_odds)
        
        total = self.count_alternating(num_odds, num_evens)
        
        if k > total:
            return []
        
        result = []
        remaining_odds = odds[:]
        remaining_evens = evens[:]
        
        # Determine starting parity
        # If num_odds > num_evens, must start with odd
        # If num_evens > num_odds, must start with even
        # If equal, can start with either
        
        k_remaining = k  # Convert to 0-indexed
        
        # Build the permutation digit by digit
        start_with_odd = num_odds > num_evens or (num_odds == num_evens and k_remaining <= self.factorial(num_odds) * self.factorial(num_evens))
        
        if num_odds == num_evens:
            # Can start with either odd or even
            perms_starting_odd = self.factorial(num_odds) * self.factorial(num_evens)
            if k_remaining <= perms_starting_odd:
                start_with_odd = True
            else:
                start_with_odd = False
                k_remaining -= perms_starting_odd
        
        # Build permutation
        use_odd = start_with_odd
        position = 0
        
        while position < n:
            if use_odd:
                # Choose from odds
                nums = remaining_odds
            else:
                # Choose from evens
                nums = remaining_evens
            
            # How many numbers to choose from
            count = len(nums)
            
            # How many alternating perms can we form with the remaining numbers?
            remaining_odd_count = len(remaining_odds)
            remaining_even_count = len(remaining_evens)
            
            if use_odd:
                remaining_odd_count -= 1
            else:
                remaining_even_count -= 1
            
            # Find which number to pick
            for i, num in enumerate(nums):
                # If we pick nums[i], how many valid continuations?
                perms_with_this_choice = self.count_alternating_with_parity(
                    remaining_odd_count, remaining_even_count, not use_odd
                )
                
                if k_remaining <= perms_with_this_choice:
                    result.append(num)
                    nums.remove(num)
                    position += 1
                    use_odd = not use_odd
                    break
                else:
                    k_remaining -= perms_with_this_choice
        
        return result
    
    def count_alternating(self, num_odds, num_evens):
        """Count total alternating permutations with given odd/even counts."""
        count = 0
        
        # Starting with odd
        if num_odds > num_evens:
            count += self.factorial(num_odds) * self.factorial(num_evens)
        elif num_odds == num_evens:
            count += self.factorial(num_odds) * self.factorial(num_evens)
        
        # Starting with even
        if num_evens > num_odds:
            count += self.factorial(num_evens) * self.factorial(num_odds)
        elif num_odds == num_evens:
            count += self.factorial(num_odds) * self.factorial(num_evens)
        
        return count
    
    def count_alternating_with_parity(self, num_odds, num_evens, start_with_odd):
        """Count alternating permutations starting with given parity."""
        if start_with_odd:
            if num_odds < num_evens:
                return 0
            if num_odds == num_evens:
                return self.factorial(num_odds) * self.factorial(num_evens)
            if num_odds == num_evens + 1:
                return self.factorial(num_odds) * self.factorial(num_evens)
            return 0
        else:
            if num_evens < num_odds:
                return 0
            if num_odds == num_evens:
                return self.factorial(num_odds) * self.factorial(num_evens)
            if num_evens == num_odds + 1:
                return self.factorial(num_odds) * self.factorial(num_evens)
            return 0
    
    def factorial(self, n):
        """Calculate factorial, capped at a large value to avoid overflow."""
        if n > 20:
            return 10**18  # Large number
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
