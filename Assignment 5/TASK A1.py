"""Task A1: End-to-End Delay Breakdown and Bandwidth-Delay Product (BDP) Calculator."""

def delay_breakdown(packet_bytes=1500, distance_km=2000, routers=3,
                    q_ms=0.5, proc_ms=0.1, rate_mbps=100):
    bits = packet_bytes * 8
    links = routers + 1
    speed_m_s = 2e8
    d_trans = (bits / (rate_mbps * 1e6)) * 1000 * links
    d_prop = ((distance_km * 1000) / speed_m_s) * 1000
    d_queue = routers * q_ms
    d_proc = routers * proc_ms
    total = d_trans + d_prop + d_queue + d_proc
    print(f"--- Delay Breakdown at {rate_mbps} Mbps ---")
    print(f"Transmission: {d_trans:.3f} ms | Propagation: {d_prop:.3f} ms | "
          f"Queuing: {d_queue:.3f} ms | Processing: {d_proc:.3f} ms | Total: {total:.3f} ms")

def bdp_analysis(rate_gbps=1.0, rtt_ms=80, tcp_win_kb=64):
    bdp_bits = (rate_gbps * 1e9) * (rtt_ms / 1000.0)
    bdp_mb = bdp_bits / (8 * 1e6)
    max_tput_mbps = (tcp_win_kb * 1024 * 8) / (rtt_ms / 1000.0) / 1e6
    util_pct = (max_tput_mbps / (rate_gbps * 1000)) * 100
    print(f"\n--- BDP & TCP Window Analysis ({rate_gbps} Gbps, {rtt_ms} ms RTT) ---")
    print(f"BDP: {bdp_bits:,.0f} bits ({bdp_mb:.2f} MB)")
    print(f"Max Throughput with {tcp_win_kb} KB Window: {max_tput_mbps:.2f} Mbps ({util_pct:.2f}% utilisation)")

if __name__ == "__main__":
    delay_breakdown(rate_mbps=100)
    delay_breakdown(rate_mbps=1000)
    bdp_analysis()
