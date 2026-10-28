from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Separate odd and even numbers
        odds = [i for i in range(1, n + 1) if i % 2 == 1]
        evens = [i for i in range(1, n + 1) if i % 2 == 0]
        
        # Count total alternating permutations
        # An alternating permutation can start with either odd or even
        # We need to count permutations that alternate between odd/even and even/odd
        
        total_count = self._count_alternating(len(odds), len(evens))
        
        if k > total_count:
            return []
        
        result = []
        remaining_k = k
        odds_copy = sorted(odds)
        evens_copy = sorted(evens)
        
        # Try to build the permutation greedily
        # At each position, try to place the smallest available number that maintains alternating property
        last_parity = None  # None = start, 0 = even, 1 = odd
        
        for pos in range(n):
            # We need to choose from remaining odds or evens
            # Count how many permutations start with each option
            
            if last_parity is None:
                # First position: try odds first (lexicographically)
                # Count permutations starting with the smallest available odd
                count_starting_odd = self._count_alternating(len(odds_copy) - 1, len(evens_copy)) if odds_copy else 0
                
                if remaining_k <= count_starting_odd and odds_copy:
                    # Use an odd number
                    val = odds_copy.pop(0)
                    result.append(val)
                    last_parity = 1
                else:
                    # Use an even number
                    remaining_k -= count_starting_odd if odds_copy else 0
                    val = evens_copy.pop(0)
                    result.append(val)
                    last_parity = 0
            elif last_parity == 1:
                # Last was odd, need even
                val = evens_copy.pop(0)
                result.append(val)
                last_parity = 0
            else:
                # Last was even, need odd
                val = odds_copy.pop(0)
                result.append(val)
                last_parity = 1
        
        return result
    
    def _count_alternating(self, num_odds: int, num_evens: int) -> int:
        """
        Count the number of alternating permutations with given number of odds and evens.
        An alternating permutation alternates between odd and even.
        """
        if num_odds < 0 or num_evens < 0:
            return 0
        if num_odds == 0 and num_evens == 0:
            return 1
        if abs(num_odds - num_evens) > 1:
            # Can't form alternating permutation if difference is more than 1
            return 0
        
        # For alternating permutation:
        # - If starting with odd: need odd-even-odd-even...
        #   This is possible if num_odds = num_evens or num_odds = num_evens + 1
        # - If starting with even: need even-odd-even-odd...
        #   This is possible if num_evens = num_odds or num_evens = num_odds + 1
        
        count = 0
        
        # Count permutations starting with odd
        if num_odds > num_evens:
            # Can start with odd: odd-even-odd-even... structure
            count += self._count_permutations_alt_start_with_odd(num_odds, num_evens)
        elif num_odds == num_evens:
            # Can start with odd and alternate perfectly
            count += self._count_permutations_alt_start_with_odd(num_odds, num_evens)
        
        # Count permutations starting with even
        if num_evens > num_odds:
            # Can start with even: even-odd-even-odd... structure
            count += self._count_permutations_alt_start_with_even(num_evens, num_odds)
        elif num_odds == num_evens:
            # Can start with even and alternate perfectly
            count += self._count_permutations_alt_start_with_even(num_evens, num_odds)
        
        return count
    
    def _count_permutations_alt_start_with_odd(self, num_odds: int, num_evens: int) -> int:
        """Count alternating permutations starting with odd."""
        if num_odds != num_evens and num_odds != num_evens + 1:
            return 0
        # Pattern: O E O E O E ...
        # Number of ways = num_odds! * num_evens!
        return self._factorial(num_odds) * self._factorial(num_evens)
    
    def _count_permutations_alt_start_with_even(self, num_evens: int, num_odds: int) -> int:
        """Count alternating permutations starting with even."""
        if num_evens != num_odds and num_evens != num_odds + 1:
            return 0
        # Pattern: E O E O E O ...
        # Number of ways = num_evens! * num_odds!
        return self._factorial(num_evens) * self._factorial(num_odds)
    
    def _factorial(self, n: int) -> int:
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
