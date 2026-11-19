"""Task 2: Compare hospital topologies and test link failures."""
from itertools import combinations
from collections import deque

NAMES = ["Emergency", "Outpatient", "Theatres", "Laboratory", "Administration"]

def build_links(kind, n=5):
    nodes = list(range(n))
    if kind == "bus":
        return [(i, i + 1) for i in range(n - 1)]
    if kind == "ring":
        return [(i, (i + 1) % n) for i in range(n)]
    if kind == "star":
        hub = n - 1  
        return [(hub, i) for i in range(n) if i != hub]
    if kind == "mesh":
        return list(combinations(nodes, 2))
    if kind == "hybrid":
        return [(4, 0), (4, 2), (0, 2), (4, 1), (4, 3)]
    raise ValueError("Unknown topology")

def reachable(edges, start, goal, failed=None):
    graph = {i: [] for i in range(5)}
    for a, b in edges:
        if failed is not None and {a, b} == set(failed):
            continue
        graph[a].append(b)
        graph[b].append(a)
    seen = {start}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == goal:
            return True
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return False

def report():
    link_cost = 96000
    for kind in ("bus", "ring", "star", "mesh", "hybrid"):
        edges = build_links(kind)
        protected = sum(
            reachable(edges, 0, 4, failed=edge) and
            reachable(edges, 2, 4, failed=edge)
            for edge in edges
        )
        print(f"{kind:7} links={len(edges):2} ports={2*len(edges):2} "
              f"estimated_cost=Rs {len(edges)*link_cost:,} "
              f"single_cut_tests_passed={protected}/{len(edges)}")

    print("\nHybrid topology links:")
    for a, b in build_links("hybrid"):
        print(f"  {NAMES[a]} <-> {NAMES[b]}")

    print("\nEmergency and Theatres remain connected to Administration")
    print("after every single link cut in the hybrid topology.")

if __name__ == "__main__":
    report()
