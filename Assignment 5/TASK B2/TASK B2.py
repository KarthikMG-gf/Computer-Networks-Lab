"""Task B2: Bottleneck Link Simulation (FIFO vs. Strict Priority Queueing for Voice)."""
import heapq

def simulate_bottleneck(link_mbps=2.0, num_calls=10, prop_ms=10.0,
                        with_download=True, strict_priority=False, duration_s=5.0):
    rate_bps = link_mbps * 1e6
    buf_limit = 60
    queue = []  # (priority, arrival_ms, size_bytes, is_voice)
    events = []  # (time_ms, event_type, call_id)

    for c in range(num_calls):
        t = (c * 20.0) / num_calls
        while t < duration_s * 1000:
            heapq.heappush(events, (t, "VOICE", c))
            t += 20.0
    if with_download:
        heapq.heappush(events, (0.0, "DATA", -1))

    server_busy_until = 0.0
    v_sent = v_drop = 0
    v_delays = []
    d_bytes = 0

    while events:
        now, etype, cid = heapq.heappop(events)
        # Drain queue up to 'now'
        while queue and server_busy_until <= now:
            prio, arr, sz, is_v = heapq.heappop(queue)
            start = max(arr, server_busy_until)
            tx_ms = (sz * 8 / rate_bps) * 1000.0
            server_busy_until = start + tx_ms
            if is_v:
                v_delays.append((server_busy_until - arr) + prop_ms)
            else:
                d_bytes += sz

        if etype == "VOICE":
            v_sent += 1
            if len(queue) < buf_limit:
                heapq.heappush(queue, (0 if strict_priority else 1, now, 200, True))
            else:
                v_drop += 1
        elif etype == "DATA":
            if len(queue) < buf_limit:
                heapq.heappush(queue, (1, now, 1500, False))
            if now + 6.0 < duration_s * 1000:
                heapq.heappush(events, (now + 6.0, "DATA", -1))

    avg_d = sum(v_delays) / len(v_delays) if v_delays else 0
    loss_pct = 100.0 * v_drop / v_sent if v_sent else 0
    d_mbps = (d_bytes * 8) / (duration_s * 1e6)
    return avg_d, loss_pct, d_mbps

if __name__ == "__main__":
    for label, dl, prio in [
        ("FIFO, No Download", False, False),
        ("FIFO + Download", True, False),
        ("Priority Queue + Download", True, True),
    ]:
        d, l, tput = simulate_bottleneck(with_download=dl, strict_priority=prio)
        print(f"{label:<26} | Voice Delay: {d:6.1f} ms | Loss: {l:5.1f}% | Download: {tput:.2f} Mbps")
