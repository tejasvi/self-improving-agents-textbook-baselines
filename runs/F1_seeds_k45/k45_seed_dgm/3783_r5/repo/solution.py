from typing import List
import math

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        """
        Find the k-th alternating permutation of [1, 2, ..., n] in lexicographical order.
        
        An alternating permutation has no two adjacent elements with the same parity.
        
        Algorithm:
        1. Count odd and even numbers
        2. Calculate total number of valid permutations
        3. If k exceeds the total, return empty list
        4. Determine if we start with odd or even
        5. Use factoradic representation to build the k-th permutation
        """
        
        # Separate odd and even numbers
        odds = list(range(1, n + 1, 2))  # [1, 3, 5, ...]
        evens = list(range(2, n + 1, 2))  # [2, 4, 6, ...]
        
        num_odds = len(odds)
        num_evens = len(evens)
        
        # Calculate factorials
        fact_odds = math.factorial(num_odds)
        fact_evens = math.factorial(num_evens)
        
        # Total alternating permutations
        # Two patterns: start with odd or start with even
        # Each pattern has fact_odds * fact_evens valid permutations
        if num_odds >= num_evens:
            # Can start with odd: odd-even-odd-even-...
            total_odds_first = fact_odds * fact_evens
            # Can start with even only if num_odds == num_evens
            total_evens_first = fact_odds * fact_evens if num_odds == num_evens else 0
        else:
            # num_evens > num_odds, can only start with even
            total_odds_first = 0
            total_evens_first = fact_odds * fact_evens
        
        total = total_odds_first + total_evens_first
        
        if k > total:
            return []
        
        result = []
        
        # Determine if we start with odd or even
        if k <= total_odds_first:
            # Start with odd
            start_with_odd = True
            k_adjusted = k
        else:
            # Start with even
            start_with_odd = False
            k_adjusted = k - total_odds_first
        
        # Use factoradic to generate the k-th permutation
        if start_with_odd:
            result = self._kth_alternating(odds, evens, k_adjusted, start_odd=True)
        else:
            result = self._kth_alternating(odds, evens, k_adjusted, start_odd=False)
        
        return result
    
    def _kth_alternating(self, odds: List[int], evens: List[int], k: int, start_odd: bool) -> List[int]:
        """
        Generate the k-th alternating permutation using factoradic representation.
        
        k is 1-indexed and adjusted for the specific pattern.
        """
        if start_odd:
            first = odds[:]
            second = evens[:]
        else:
            first = evens[:]
            second = odds[:]
        
        # Convert k to 0-indexed
        k = k - 1
        
        # Generate the k-th permutation using factoradic
        result = []
        
        # We need to interleave selections from first and second lists
        # Length of first >= length of second
        num_first = len(first)
        num_second = len(second)
        
        # Get factoradic representation of k
        factoradic = self._to_factoradic(k, num_first + num_second)
        
        # Use factoradic to select elements
        available_first = list(range(num_first))
        available_second = list(range(num_second))
        
        for i in range(num_first + num_second):
            if i % 2 == 0:  # Pick from first list
                idx = factoradic[i] % len(available_first)
                result.append(first[available_first.pop(idx)])
            else:  # Pick from second list
                idx = factoradic[i] % len(available_second)
                result.append(second[available_second.pop(idx)])
        
        return result
    
    def _to_factoradic(self, n: int, length: int) -> List[int]:
        """
        Convert a number to its factoradic representation.
        Returns a list of digits where digit[i] is in range [0, i].
        """
        factoradic = []
        k = n
        for i in range(length - 1, 0, -1):
            factoradic.append(k % (i + 1))
            k //= (i + 1)
        factoradic.append(k)
        return list(reversed(factoradic))
    
    def _kth_permutation_factoradic(self, elements: List[int], k: int) -> List[int]:
        """
        Generate the k-th permutation of elements using factoradic representation.
        k is 1-indexed.
        """
        k = k - 1  # Convert to 0-indexed
        n = len(elements)
        result = []
        available = list(range(n))
        
        factoradic = self._to_factoradic(k, n)
        
        for i in range(n):
            idx = factoradic[i]
            if idx >= len(available):
                idx = len(available) - 1
            result.append(elements[available.pop(idx)])
        
        return result
