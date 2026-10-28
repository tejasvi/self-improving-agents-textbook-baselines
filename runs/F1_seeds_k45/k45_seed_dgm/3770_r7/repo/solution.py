class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        result_len = n + m - 1
        
        # Build result character by character using backtracking
        result = []
        if self._backtrack(result, str1, str2, 0):
            return ''.join(result)
        else:
            return ""
    
    def _backtrack(self, result, str1, str2, pos):
        """
        Recursively build the result string.
        Returns True if a valid string can be built, False otherwise.
        """
        n = len(str1)
        m = len(str2)
        result_len = n + m - 1
        
        # Base case: we've filled all positions
        if pos == result_len:
            return True
        
        # Try each character from 'a' to 'z'
        for char_code in range(ord('a'), ord('z') + 1):
            result.append(chr(char_code))
            
            # Check if this partial assignment is still valid
            if self._is_valid_so_far(result, str1, str2, pos):
                # Recursively try to fill the rest
                if self._backtrack(result, str1, str2, pos + 1):
                    return True
            
            result.pop()
        
        return False
    
    def _is_valid_so_far(self, result, str1, str2, last_pos):
        """
        Check if the current partial assignment is valid.
        A constraint can be checked if the entire substring is filled.
        """
        n = len(str1)
        m = len(str2)
        
        # Check all constraints that are now completely determined
        for i in range(n):
            if i + m - 1 <= last_pos:  # This substring is completely filled
                substring = ''.join(result[i:i+m])
                if str1[i] == 'T' and substring != str2:
                    return False
                if str1[i] == 'F' and substring == str2:
                    return False
        
        return True
