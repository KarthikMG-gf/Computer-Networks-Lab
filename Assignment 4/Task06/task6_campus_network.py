"""Task 6: University campus traffic sizing, address plan and redundancy model."""
from collections import deque
import math

BUILDINGS = {
    "Academic": 1.6,
    "Laboratories": 2.1,
    "Library": 0.6,
    "Auditorium": 1.0,
    "Hostels": 9.6,
    "DataCentre": 3.0,
}

def traffic_summary():
    daytime = sum(BUILDINGS[k] for k in
                  ("Academic", "Laboratories", "Library", "Auditorium"))
    evening = BUILDINGS["Hostels"] + BUILDINGS["Library"]
    internet_peak = evening * 0.50
    print("Campus traffic estimate (Gbps)")
    print(f"  Daytime buildings: {daytime:.1f}")
    print(f"  Evening hostels + library: {evening:.1f}")
    print(f"  Approx. internet peak at 50% external traffic: {internet_peak:.1f}")

def address_plan():
    vlans = {
        "Academic Student": ("10.1.0.0", 21),
        "Academic Staff": ("10.1.8.0", 24),
        "Academic Guest": ("10.1.9.0", 24),
        "Academic CCTV": ("10.1.10.0", 24),
        "Lab PCs": ("10.2.0.0", 22),
        "Lab Staff": ("10.2.4.0", 24),
        "Lab Student WiFi": ("10.2.5.0", 24),
        "Lab Guest": ("10.2.6.0", 25),
    }
    print("\nCampus VLAN address plan")
    for name, (network, prefix) in vlans.items():
        print(f"  {name:22} {network}/{prefix}")

def path_exists(graph, start, goal, failed_edge=None):
    q, seen = deque([start]), {start}
    while q:
        node = q.popleft()
        if node == goal:
            return True
        for nxt in graph.get(node, []):
            if failed_edge and {node, nxt} == set(failed_edge):
                continue
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return False

def redundancy_test():
    graph = {
        "DIST-AC": ["CORE-1", "CORE-2"],
        "CORE-1": ["DIST-AC", "CORE-2", "EDGE-A"],
        "CORE-2": ["DIST-AC", "CORE-1", "EDGE-B"],
        "EDGE-A": ["CORE-1", "ISP-A"],
        "EDGE-B": ["CORE-2", "ISP-B"],
        "ISP-A": ["EDGE-A"],
        "ISP-B": ["EDGE-B"],
    }
    print("\nRedundancy tests from DIST-AC to internet")
    for failed in (None, ("DIST-AC", "CORE-1"), ("CORE-1", "EDGE-A")):
        ok_a = path_exists(graph, "DIST-AC", "ISP-A", failed)
        ok_b = path_exists(graph, "DIST-AC", "ISP-B", failed)
        label = "no failure" if failed is None else f"failure {failed[0]}-{failed[1]}"
        print(f"  {label:28}: ISP-A={ok_a}, ISP-B={ok_b}, any_path={ok_a or ok_b}")

def main():
    traffic_summary()
    address_plan()
    redundancy_test()
    print("\nOversubscription examples:")
    print(f"  Access: 48 Gbps / 20 Gbps = {48/20:.1f}:1")
    print(f"  Academic distribution: 140 Gbps / 80 Gbps = {140/80:.2f}:1")
    print(f"  Internet with two 3 Gbps ISPs: 5.1 / 6 = {5.1/6:.2%} utilisation")

if __name__ == "__main__":
    main()
