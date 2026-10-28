from collections import defaultdict

def tarjan_scc(graph, nodes):
    """Find strongly connected components using Tarjan's algorithm"""
    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    on_stack = defaultdict(bool)
    sccs = []
    
    def strongconnect(v):
        index[v] = index_counter[0]
        lowlinks[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack[v] = True
        
        for w in graph[v]:
            if w not in index:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif on_stack[w]:
                lowlinks[v] = min(lowlinks[v], index[w])
        
        if lowlinks[v] == index[v]:
            component = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                component.append(w)
                if w == v:
                    break
            sccs.append(component)
    
    for v in nodes:
        if v not in index:
            strongconnect(v)
    
    return sccs

def solve():
    n = int(input())
    
    # Build the graph
    graph = defaultdict(set)  # adjacency list
    all_nodes = set()
    
    for _ in range(n):
        s = input().strip()
        u, v = s[0], s[1]
        
        graph[u].add(v)
        all_nodes.add(u)
        all_nodes.add(v)
    
    # Find strongly connected components
    sccs = tarjan_scc(graph, all_nodes)
    
    # Create mapping from node to SCC ID
    scc_id = {}
    for i, scc in enumerate(sccs):
        for node in scc:
            scc_id[node] = i
    
    # Find inter-SCC edges
    scc_has_in = [False] * len(sccs)
    scc_has_out = [False] * len(sccs)
    
    for u in graph:
        for v in graph[u]:
            if scc_id[u] != scc_id[v]:
                # This is an inter-SCC edge
                scc_has_out[scc_id[u]] = True
                scc_has_in[scc_id[v]] = True
    
    # Count sources (SCC with no incoming inter-SCC edges)
    # and sinks (SCC with no outgoing inter-SCC edges)
    num_sources = sum(1 for i in range(len(sccs)) if not scc_has_in[i])
    num_sinks = sum(1 for i in range(len(sccs)) if not scc_has_out[i])
    
    # The minimum paths is the maximum of sources and sinks
    result = max(num_sources, num_sinks)
    print(result)

solve()
