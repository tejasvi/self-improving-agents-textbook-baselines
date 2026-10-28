class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        """
        Generate lexicographically smallest string that satisfies constraints.
        
        The generated string has length n + m - 1.
        For each position i in [0, n):
        - If str1[i] == 'T': word[i:i+m] must equal str2
        - If str1[i] == 'F': word[i:i+m] must NOT equal str2
        """
        n = len(str1)
        m = len(str2)
        result_len = n + m - 1
        
        # Use backtracking to build the string greedily
        word = ['a'] * result_len
        
        if self._backtrack(str1, str2, word, 0):
            return ''.join(word)
        else:
            return ""
    
    def _backtrack(self, str1: str, str2: str, word: list, pos: int) -> bool:
        """
        Backtracking function to find lexicographically smallest valid string.
        Returns True if a valid string is found, False otherwise.
        """
        n = len(str1)
        m = len(str2)
        result_len = len(word)
        
        if pos == result_len:
            # Check if all constraints are satisfied
            for i in range(n):
                substring = word[i:i+m]
                if str1[i] == 'T' and substring != list(str2):
                    return False
                if str1[i] == 'F' and substring == list(str2):
                    return False
            return True
        
        # Try characters from 'a' to 'z'
        for ch in 'abcdefghijklmnopqrstuvwxyz':
            word[pos] = ch
            
            # Check if current assignment violates any completed constraints
            valid = True
            
            # Check all constraints that are now complete
            for i in range(n):
                if i + m - 1 <= pos:  # Constraint at position i is complete
                    substring = word[i:i+m]
                    if str1[i] == 'T' and substring != list(str2):
                        valid = False
                        break
                    if str1[i] == 'F' and substring == list(str2):
                        valid = False
                        break
            
            if valid:
                if self._backtrack(str1, str2, word, pos + 1):
                    return True
        
        return False
