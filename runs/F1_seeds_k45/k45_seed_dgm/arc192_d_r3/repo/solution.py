from math import gcd

MOD = 998244353

def get_divisors(n):
    """Get all divisors of n"""
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(divisors)

def factorize(n):
    """Get all coprime factorizations of n: (p, q) where p*q=n and gcd(p,q)=1"""
    divisors = get_divisors(n)
    factorizations = []
    for p in divisors:
        q = n // p
        if gcd(p, q) == 1:
            factorizations.append((p, q))
    return factorizations

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # For each A_i, get all possible (p_i, q_i) pairs where gcd(p_i, q_i) = 1 and p_i * q_i = A_i
    factorizations = []
    for a in A:
        factorizations.append(factorize(a))
    
    total_score = 0
    
    def backtrack(pos, pq_sequence, multipliers):
        """
        pos: current position in A (0 to N-1, where N-1 is the last A value)
        pq_sequence: list of (p, q) pairs chosen so far
        multipliers: list of multipliers k_i chosen so far
        """
        nonlocal total_score
        
        if pos == len(A):
            # We've chosen all factorizations and multipliers
            # Now construct the sequence S
            sequence = []
            for i in range(len(pq_sequence)):
                p_i, q_i = pq_sequence[i]
                k_i = multipliers[i]
                sequence.append(p_i * k_i)
            
            # The last element is determined by the last q and multiplier
            p_last, q_last = pq_sequence[-1]
            k_last = multipliers[-1]
            sequence.append(q_last * k_last)
            
            # Check if gcd of entire sequence is 1
            g = sequence[0]
            for s in sequence[1:]:
                g = gcd(g, s)
            if g == 1:
                # Calculate score: product of all elements
                score = 1
                for s in sequence:
                    score = (score * s) % MOD
                total_score = (total_score + score) % MOD
            return
        
        # Try all factorizations of A[pos]
        for p_pos, q_pos in factorizations[pos]:
            pq_sequence.append((p_pos, q_pos))
            
            if pos == 0:
                # For the first position, we can choose any multiplier
                # But we need to ensure the gcd constraint at the end
                # For now, let's try all reasonable multipliers
                # The multiplier should relate the scaling
                
                # Actually, let's think differently:
                # We can choose k_0 freely for the first element
                # But we need to consider the constraint from the next element
                
                # Let's enumerate multipliers based on divisibility constraints
                
                # For now, let's try small multipliers
                for k0 in range(1, 100):  # This is a rough upper bound
                    multipliers.append(k0)
                    backtrack(pos + 1, pq_sequence, multipliers)
                    multipliers.pop()
            else:
                # At position pos >= 1, we have a constraint:
                # The previous q_{pos-1} and previous k_{pos-1} must satisfy:
                # q_{pos-1} * k_{pos-1} = p_pos * k_pos
                
                # So: k_pos = (q_{pos-1} * k_{pos-1}) / p_pos
                
                p_prev, q_prev = pq_sequence[pos - 1]
                k_prev = multipliers[pos - 1]
                
                numerator = q_prev * k_prev
                
                if numerator % p_pos == 0:
                    k_pos = numerator // p_pos
                    multipliers.append(k_pos)
                    backtrack(pos + 1, pq_sequence, multipliers)
                    multipliers.pop()
            
            pq_sequence.pop()
    
    backtrack(0, [], [])
    print(total_score)

solve()
