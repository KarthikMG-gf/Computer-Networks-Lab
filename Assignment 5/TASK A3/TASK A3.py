"""Task A3: Client-Server vs. P2P Distribution Time & VoIP Capacity Calculator."""

def distribution_times(file_gb=4, peers=20, u_server_mbps=100, d_peer_mbps=50, u_peer_mbps=20):
    F = file_gb * 8000  # Mbits (decimal GB)
    d_cs = max((peers * F) / u_server_mbps, F / d_peer_mbps)
    d_p2p = max(F / u_server_mbps, F / d_peer_mbps, (peers * F) / (u_server_mbps + peers * u_peer_mbps))
    print(f"Client-Server Min Distribution Time : {d_cs:.0f} s")
    print(f"Peer-to-Peer Min Distribution Time  : {d_p2p:.0f} s (Speedup: {d_cs/d_p2p:.1f}x)")

def voip_capacity(codec_kbps=64, packet_ms=20, header_bytes=40, link_mbps=2.0):
    pps = 1000 / packet_ms
    payload_bytes = (codec_kbps * 1000 * (packet_ms / 1000.0)) / 8
    ip_pkt_bytes = payload_bytes + header_bytes
    eth_pkt_bytes = ip_pkt_bytes + 18
    bw_ip_kbps = (ip_pkt_bytes * 8 * pps) / 1000.0
    bw_eth_kbps = (eth_pkt_bytes * 8 * pps) / 1000.0
    print(f"\nVoIP PPS: {pps:.0f} pkt/s | IP Bandwidth: {bw_ip_kbps:.1f} kbps | Ethernet Bandwidth: {bw_eth_kbps:.1f} kbps")
    print(f"Max Calls on {link_mbps} Mbps link: {int((link_mbps*1000)//bw_ip_kbps)} (IP) / {int((link_mbps*1000)//bw_eth_kbps)} (Ethernet)")

if __name__ == "__main__":
    distribution_times()
    voip_capacity()
