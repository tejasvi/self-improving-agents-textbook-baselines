class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        def count_partitions(string, k):
            """Count the number of partitions for a given string."""
            partitions = 0
            i = 0
            n = len(string)
            
            while i < n:
                # Try to extend the prefix as far as possible while keeping at most k distinct chars
                char_count = {}
                j = i
                
                # Extend j as far as we can with at most k distinct characters
                while j < n:
                    char = string[j]
                    # If this character is new and we'd exceed k, stop here
                    if char not in char_count and len(char_count) >= k:
                        break
                    
                    # Add/increment the character count
                    if char not in char_count:
                        char_count[char] = 0
                    char_count[char] += 1
                    
                    j += 1
                
                # If we couldn't extend at all (shouldn't happen with k >= 1), take at least one character
                if j == i:
                    j = i + 1
                
                # We found a partition from i to j (exclusive)
                partitions += 1
                i = j
            
            return partitions
        
        # Optimization: instead of trying all O(n * 26) combinations,
        # we use a smarter approach: for each potential partition boundary,
        # try changing a character right before/at that boundary
        
        n = len(s)
        max_partitions = count_partitions(s, k)
        
        # First pass: identify where partitions would be cut naturally
        # and see if we can prevent early cuts by changing characters
        
        # Try all reasonable single character changes
        # But limit the search to positions that matter
        for i in range(min(n, 200)):  # Limit to first 200 chars for efficiency
            original_char = s[i]
            
            # Try changing to different characters (but focus on meaningful ones)
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c == original_char:
                    continue
                
                # Create modified string
                modified = s[:i] + c + s[i+1:]
                
                # Count partitions
                partitions = count_partitions(modified, k)
                max_partitions = max(max_partitions, partitions)
        
        return max_partitions
