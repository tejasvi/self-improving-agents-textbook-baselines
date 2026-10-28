from typing import List
import math

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        """
        Find the k-th alternating permutation of numbers 1 to n in lexicographical order.
        An alternating permutation has no two adjacent elements both odd or both even.
        """
        
        # Separate odd and even numbers
        odds = [i for i in range(1, n + 1) if i % 2 == 1]
        evens = [i for i in range(1, n + 1) if i % 2 == 0]
        
        num_odds = len(odds)
        num_evens = len(evens)
        
        # Calculate factorial
        def factorial(x):
            if x <= 1:
                return 1
            result = 1
            for i in range(2, x + 1):
                result *= i
            return result
        
        # Total number of alternating permutations
        # Starting with odd or even, then alternating
        # If we start with odd: num_odds! * num_evens! ways
        # If we start with even: num_evens! * num_odds! ways
        perms_per_start = factorial(num_odds) * factorial(num_evens)
        total_perms = perms_per_start * 2 if num_odds == num_evens else perms_per_start
        
        # Check if k is valid
        if k > total_perms:
            return []
        
        result = []
        remaining_odds = odds[:]
        remaining_evens = evens[:]
        
        # Determine if we start with odd or even
        # For lexicographical order, we want to start with smallest possible
        # When both are possible (num_odds == num_evens or similar), we choose based on k
        
        if num_odds > num_evens:
            # Must start with odd
            start_with_odd = True
        elif num_evens > num_odds:
            # Must start with even
            start_with_odd = False
        else:
            # Can start with either, determine by k
            if k <= perms_per_start:
                start_with_odd = True
            else:
                start_with_odd = False
                k -= perms_per_start
        
        # Build the permutation greedily
        is_odd_turn = start_with_odd
        
        while remaining_odds or remaining_evens:
            if is_odd_turn:
                # Pick from odd numbers
                # How many permutations start with each remaining odd?
                perms_per_choice = factorial(len(remaining_odds) - 1) * factorial(len(remaining_evens))
                
                # Find which odd to pick
                choice_idx = (k - 1) // perms_per_choice
                result.append(remaining_odds[choice_idx])
                k = ((k - 1) % perms_per_choice) + 1
                remaining_odds.pop(choice_idx)
                is_odd_turn = False
            else:
                # Pick from even numbers
                perms_per_choice = factorial(len(remaining_odds)) * factorial(len(remaining_evens) - 1)
                
                # Find which even to pick
                choice_idx = (k - 1) // perms_per_choice
                result.append(remaining_evens[choice_idx])
                k = ((k - 1) % perms_per_choice) + 1
                remaining_evens.pop(choice_idx)
                is_odd_turn = True
        
        return result
