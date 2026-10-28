class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        """
        Key insight: For each conflicting pair [a, b] where a < b,
        a subarray contains both a and b if and only if:
        - start position <= a
        - end position >= b
        
        So the count of bad subarrays for pair [a, b] = a * (n - b + 1)
        
        For multiple pairs, we need to count subarrays that violate AT LEAST ONE pair.
        We use a different approach: iterate through positions and track which pairs are "active"
        """
        
        def count_valid_subarrays(pairs):
            """
            Count valid subarrays given a list of conflicting pairs.
            We'll iterate through all possible subarrays and check validity.
            """
            if not pairs:
                return n * (n + 1) // 2
            
            # Normalize pairs: ensure first < second
            normalized = set()
            for a, b in pairs:
                normalized.add((min(a, b), max(a, b)))
            
            valid_count = 0
            
            # Iterate through all subarrays [i, j] in 1-indexed form
            for i in range(1, n + 1):
                for j in range(i, n + 1):
                    # Check if subarray [i, j] contains any conflicting pair
                    is_valid = True
                    for a, b in normalized:
                        if a >= i and b <= j:
                            is_valid = False
                            break
                    if is_valid:
                        valid_count += 1
            
            return valid_count
        
        max_valid = 0
        
        # Try removing each conflicting pair
        for i in range(len(conflictingPairs)):
            # Create new pairs list without element at index i
            remaining_pairs = conflictingPairs[:i] + conflictingPairs[i+1:]
            valid_count = count_valid_subarrays(remaining_pairs)
            max_valid = max(max_valid, valid_count)
        
        return max_valid
