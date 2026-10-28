class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        result_len = n + m - 1
        
        # Try to build the result greedily with backtracking
        result = ['a'] * result_len
        
        def is_valid():
            """Check if current result satisfies all constraints from str1"""
            for i in range(n):
                substring = ''.join(result[i:i+m])
                if str1[i] == 'T' and substring != str2:
                    return False
                if str1[i] == 'F' and substring == str2:
                    return False
            return True
        
        def can_extend(pos):
            """Check if we can extend to position pos with current result"""
            # Check all constraints that are now fully determined
            for i in range(max(0, pos - m + 1), min(n, pos + 1)):
                # Check if substring starting at i is fully determined
                if i + m - 1 <= pos:
                    substring = ''.join(result[i:i+m])
                    if str1[i] == 'T' and substring != str2:
                        return False
                    if str1[i] == 'F' and substring == str2:
                        return False
            return True
        
        def backtrack(pos):
            """Build result string using backtracking"""
            if pos == result_len:
                return is_valid()
            
            # For 'T' constraints, if this position starts a required substring
            must_match = False
            for i in range(max(0, pos - m + 1), min(n, pos + 1)):
                if i + m - 1 == pos and str1[i] == 'T':
                    must_match = True
                    break
            
            if must_match:
                # Find which constraint requires matching
                for i in range(max(0, pos - m + 1), min(n, pos + 1)):
                    if i + m - 1 == pos and str1[i] == 'T':
                        # This position must complete substring str2
                        required_char = str2[pos - i]
                        result[pos] = required_char
                        if can_extend(pos) and backtrack(pos + 1):
                            return True
                        result[pos] = 'a'
                        return False
            else:
                # Try characters from 'a' to 'z'
                for ch in 'abcdefghijklmnopqrstuvwxyz':
                    result[pos] = ch
                    if can_extend(pos) and backtrack(pos + 1):
                        return True
                result[pos] = 'a'
                return False
        
        if backtrack(0):
            return ''.join(result)
        return ""
