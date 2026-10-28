class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        result_len = n + m - 1
        
        # Step 1: Start with the smallest possible character ('a')
        result = ['a'] * result_len
        
        # Step 2: Enforce all 'T' constraints (mandatory)
        for i in range(n):
            if str1[i] == 'T':
                for j in range(m):
                    result[i + j] = str2[j]
        
        # Step 3: Fix any 'F' constraint violations
        # An F constraint is violated if the substring equals str2
        for i in range(n):
            if str1[i] == 'F':
                substring = ''.join(result[i:i+m])
                if substring == str2:
                    # Need to change this substring
                    # Find the rightmost position that doesn't conflict with T constraints
                    fixed = False
                    for j in range(m - 1, -1, -1):
                        pos = i + j
                        # Check if this position is constrained by a T constraint
                        is_constrained = False
                        for k in range(n):
                            if str1[k] == 'T' and k <= pos < k + m:
                                # This position is part of a T constraint
                                is_constrained = True
                                break
                        
                        if not is_constrained:
                            # We can change this position
                            # Increment the character
                            if result[pos] < 'z':
                                result[pos] = chr(ord(result[pos]) + 1)
                                fixed = True
                                break
                    
                    if not fixed:
                        # All positions in this range are constrained by T
                        # Can't satisfy this F constraint
                        return ""
        
        # Step 4: Verify all constraints
        for i in range(n):
            substring = ''.join(result[i:i+m])
            if str1[i] == 'T' and substring != str2:
                return ""
            if str1[i] == 'F' and substring == str2:
                return ""
        
        return ''.join(result)
