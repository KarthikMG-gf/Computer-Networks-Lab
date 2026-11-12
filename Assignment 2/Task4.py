"""Distance-vector routing (Bellman-Ford exchange) among five campus routers."""
INF = 99
names = "ABCDE"
cost = {("A", "B"): 2, ("A", "C"): 7, ("B", "C"): 3, ("B", "D"): 8,
        ("C", "D"): 1, ("D", "E"): 4}

def run_dv(cost_dict):
    link = {}
    for (u, v), c in cost_dict.items():
        link[u, v] = link[v, u] = c
    table = {u: {v: (0 if u == v else link.get((u, v), INF)) for v in names} for u in names}
    rounds = 0
    changed = True
    while changed:
        changed = False
        rounds += 1
        old = {u: dict(table[u]) for u in names}       # vectors received this round
        for u in names:
            for n in names:
                if (u, n) not in link:
                    continue
                for dest in names:
                    # TODO 1: Bellman-Ford update: if going through neighbour n (link cost +
                    #   n's old distance to dest) is cheaper than table[u][dest], update it
                    #   and set changed = True
                    if link[(u, n)] + old[n][dest] < table[u][dest]:
                        table[u][dest] = link[(u, n)] + old[n][dest]
                        changed = True
    print(f"converged after {rounds} rounds")
    for u in names:
        print(u, " ".join(f"{table[u][v]:2d}" for v in names))

print("=== Initial Topology ===")
run_dv(cost)

print("\n=== After Link C-D Fails (cost = 99) ===")
failed_cost = dict(cost)
failed_cost[("C", "D")] = 99
run_dv(failed_cost)
