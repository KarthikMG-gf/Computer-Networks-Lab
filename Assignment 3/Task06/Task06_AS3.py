"""Q6: Handshake latency calculator and Wi-Fi -> 5G handover comparison."""

def analyze_handshakes(rtt_ms=100):
    stacks = {
        "TCP + TLS 1.2 (Full)": 3 * rtt_ms,
        "TCP + TLS 1.3 (Full)": 2 * rtt_ms,
        "QUIC (First Visit 1-RTT)": 1 * rtt_ms,
        "QUIC (0-RTT Resumption)": 0 * rtt_ms,
    }
    for name, delay in stacks.items():
        print(f"{name:<26}: {delay:3d} ms before first request byte")

if __name__ == "__main__":
    analyze_handshakes(100)
