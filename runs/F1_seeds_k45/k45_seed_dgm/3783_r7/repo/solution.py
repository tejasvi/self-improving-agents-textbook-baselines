from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        """
        Find the k-th alternating permutation of [1, 2, ..., n] in lexicographic order.
        An alternating permutation has no two adjacent elements with the same parity.
        """
        # Separate numbers into odds and evens
        odds = [i for i in range(1, n + 1) if i % 2 == 1]
        evens = [i for i in range(1, n + 1) if i % 2 == 0]
        
        num_odds = len(odds)
        num_evens = len(evens)
        
        # Calculate total count of valid alternating permutations
        # We have num_odds! * num_evens! ways if num_odds == num_evens
        # We have num_odds! * num_evens! or num_odds! * num_evens! ways if they differ by 1
        total_count = self.count_alternating_permutations(num_odds, num_evens)
        
        if k > total_count:
            return []
        
        result = []
        # Try starting with odd
        if num_odds > num_evens:
            # Must start with odd
            result = self.build_kth_permutation(k, odds, evens, True)
        elif num_odds == num_evens:
            # Can start with either odd or even
            count_starting_odd = self.factorial(num_odds) * self.factorial(num_evens)
            if k <= count_starting_odd:
                result = self.build_kth_permutation(k, odds, evens, True)
            else:
                result = self.build_kth_permutation(k - count_starting_odd, evens, odds, True)
        else:  # num_evens > num_odds
            # Must start with even
            result = self.build_kth_permutation(k, evens, odds, True)
        
        return result
    
    def count_alternating_permutations(self, num_odds: int, num_evens: int) -> int:
        """Count total alternating permutations with given counts of odds and evens."""
        if abs(num_odds - num_evens) > 1:
            return 0
        
        fact_odd = self.factorial(num_odds)
        fact_even = self.factorial(num_evens)
        
        if num_odds == num_evens:
            # Can start with either, so count both arrangements
            return 2 * fact_odd * fact_even
        else:
            # Only one way to arrange (must start with the larger group)
            return fact_odd * fact_even
    
    def factorial(self, n: int) -> int:
        """Calculate n! with cap at a large number to avoid overflow."""
        result = 1
        for i in range(2, n + 1):
            result *= i
            if result > 10**18:  # Cap to avoid overflow
                return 10**18
        return result
    
    def build_kth_permutation(self, k: int, first_group: List[int], 
                              second_group: List[int], start_with_first: bool) -> List[int]:
        """
        Build the k-th alternating permutation starting with first_group.
        Assumes we need to alternate between first_group and second_group.
        """
        first_group = sorted(first_group)
        second_group = sorted(second_group)
        
        result = []
        used_first = [False] * len(first_group)
        used_second = [False] * len(second_group)
        
        # Build position by position
        is_first_turn = True
        
        for pos in range(len(first_group) + len(second_group)):
            if is_first_turn:
                # Choose from first_group
                remaining_first = sum(1 for x in used_first if not x)
                remaining_second = sum(1 for x in used_second if not x)
                
                # For each available number in first_group, count how many valid permutations
                # follow if we choose it
                count = 0
                for i in range(len(first_group)):
                    if not used_first[i]:
                        # If we choose this, we need to count permutations with remaining elements
                        perms_if_chosen = self.count_alternating_permutations(
                            remaining_first - 1, remaining_second
                        )
                        if count + perms_if_chosen >= k:
                            # This is the one we choose
                            result.append(first_group[i])
                            used_first[i] = True
                            k -= count
                            break
                        count += perms_if_chosen
                is_first_turn = False
            else:
                # Choose from second_group
                remaining_first = sum(1 for x in used_first if not x)
                remaining_second = sum(1 for x in used_second if not x)
                
                count = 0
                for i in range(len(second_group)):
                    if not used_second[i]:
                        perms_if_chosen = self.count_alternating_permutations(
                            remaining_first, remaining_second - 1
                        )
                        if count + perms_if_chosen >= k:
                            result.append(second_group[i])
                            used_second[i] = True
                            k -= count
                            break
                        count += perms_if_chosen
                is_first_turn = True
        
        return result
