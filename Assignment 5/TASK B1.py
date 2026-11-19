"""Task B1: Network performance metrics from a captured packet trace (e.g. from Wireshark)."""

TRACE = [
    (1, 0, 42, 1200), (2, 20, 61, 1200), (3, 40, 85, 1200),
    (4, 60, None, 1200), (5, 80, 119, 1200), (6, 100, 146, 1200),
    (7, 120, 158, 1200), (8, 140, 190, 1200), (9, 160, None, 1200),
    (10, 180, 222, 1200)
]

def metrics(trace):
    got = [(s, tx, rx, b) for s, tx, rx, b in trace if rx is not None]
    # TODO 1: Completed loss, delay, jitter, and throughput calculations
    loss = 100.0 * (len(trace) - len(got)) / len(trace)
    delays = [rx - tx for _, tx, rx, _ in got]
    avg_delay = sum(delays) / len(delays)
    jitter = sum(abs(delays[i] - delays[i - 1]) for i in range(1, len(delays))) / (len(delays) - 1)
    bits = sum(b * 8 for _, _, _, b in got)
    throughput = bits / (got[-1][2] - trace[0][1])
    return loss, avg_delay, jitter, throughput

if __name__ == "__main__":
    print("--- Original Trace (With Lost Packets 4 & 9) ---")
    loss, d, j, thr = metrics(TRACE)
    print(f"packet loss {loss:.1f} %")
    print(f"average delay {d:.1f} ms, jitter {j:.1f} ms")
    print(f"throughput {thr:.1f} kbps")
    print("VoIP quality:", "acceptable" if d < 150 and j < 30 and loss < 1 else "poor")

    print("\n--- Trace With Lost Packets Removed ---")
    clean_trace = [pkt for pkt in TRACE if pkt[2] is not None]
    loss2, d2, j2, thr2 = metrics(clean_trace)
    print(f"packet loss {loss2:.1f} %")
    print(f"average delay {d2:.1f} ms, jitter {j2:.1f} ms")
    print(f"throughput {thr2:.1f} kbps")
    print("VoIP quality:", "acceptable" if d2 < 150 and j2 < 30 and loss2 < 1 else "poor")
