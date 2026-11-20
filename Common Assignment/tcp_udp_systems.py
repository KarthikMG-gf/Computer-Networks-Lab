import socket
import threading
import time
import statistics

HOST = "127.0.0.1"
TCP_PORT = 5000
UDP_PORT = 5001


# ==================== SERVER SECTION ====================
def handle_tcp_client(conn, addr):
    print(f"[SERVER-TCP] Connection Established (3-Way Handshake) with {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            cid, msg = data.decode("utf-8").split("|", 1)
            print(f"[SERVER-TCP] Message Received from {cid}: '{msg}'")
            ack = f"ACK_OK: Server received '{msg}' from {cid}"
            conn.sendall(ack.encode("utf-8"))
    print(f"[SERVER-TCP] Connection Closed with {addr}")


def run_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, TCP_PORT))
        s.listen(5)
        print(f"[SERVER] TCP Listening on {HOST}:{TCP_PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_tcp_client, args=(conn, addr), daemon=True).start()


def run_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, UDP_PORT))
        print(f"[SERVER] UDP Listening on {HOST}:{UDP_PORT}")
        while True:
            data, addr = s.recvfrom(1024)
            cid, msg = data.decode("utf-8").split("|", 1)
            print(f"[SERVER-UDP] Message Received from {cid} ({addr}): '{msg}'")
            reply = f"UDP_ECHO: Server received '{msg}' from {cid}"
            s.sendto(reply.encode("utf-8"), addr)


# ==================== CLIENT SECTION ====================
def send_message(client_id, server_ip, port, protocol, message):
    payload = f"{client_id}|{message}".encode("utf-8")
    start_time = time.perf_counter()

    if protocol == "TCP":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect((server_ip, port))
            conn_status = "Connected (3-Way Handshake)"
            s.sendall(payload)
            msg_received = s.recv(1024).decode("utf-8")
            ack_status = "ACK Received (Guaranteed)"
    else:  # UDP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2.0)
            conn_status = "Connectionless (No Handshake)"
            s.sendto(payload, (server_ip, port))
            data, _ = s.recvfrom(1024)
            msg_received = data.decode("utf-8")
            ack_status = "No Transport ACK (App Echo Only)"

    tx_time_ms = (time.perf_counter() - start_time) * 1000

    print("\n--- CLIENT TELEMETRY ---")
    print(f"Client ID                : {client_id}")
    print(f"Server IP Address        : {server_ip}")
    print(f"Port Number              : {port}")
    print(f"Protocol Selection       : {protocol}")
    print(f"Message Input            : {message}")
    print(f"Message Received         : {msg_received}")
    print(f"Connection Status        : {conn_status}")
    print(f"Packet Transmission Time : {tx_time_ms:.4f} ms")
    print(f"Acknowledgment Status    : {ack_status}")
    return tx_time_ms


# ==================== MAIN EXECUTION & REPORT ====================
if __name__ == "__main__":
    # 1. Start concurrent TCP and UDP servers in background threads
    threading.Thread(target=run_tcp_server, daemon=True).start()
    threading.Thread(target=run_udp_server, daemon=True).start()
    time.sleep(0.3)  # Allow sockets to bind cleanly

    # 2. Simulate multiple clients sending TCP and UDP messages
    tcp_times = []
    udp_times = []

    test_cases = [
        ("CLIENT-01", HOST, TCP_PORT, "TCP", "Hello Server via TCP"),
        ("CLIENT-02", HOST, TCP_PORT, "TCP", "Reliable File Chunk #1"),
        ("CLIENT-01", HOST, UDP_PORT, "UDP", "Real-Time Sensor Frame #1"),
        ("CLIENT-02", HOST, UDP_PORT, "UDP", "Fast Voice Packet #2"),
    ]

    for cid, ip, port, proto, msg in test_cases:
        elapsed = send_message(cid, ip, port, proto, msg)
        if proto == "TCP":
            tcp_times.append(elapsed)
        else:
            udp_times.append(elapsed)
        time.sleep(0.1)

    # 3. Print Automated TCP vs UDP Comparison Report
    print("\n" + "=" * 64)
    print("                 TCP vs UDP COMPARISON REPORT                   ")
    print("=" * 64)
    print(f"{'Parameter':<26} | {'TCP':<16} | {'UDP':<16}")
    print("-" * 64)
    print(f"{'Packets Transmitted':<26} | {len(tcp_times):<16} | {len(udp_times):<16}")
    print(f"{'Avg Transmission Time':<26} | {statistics.mean(tcp_times):.4f} ms      | {statistics.mean(udp_times):.4f} ms")
    print(f"{'Connection Type':<26} | {'Connection-Based':<16} | {'Connectionless':<16}")
    print(f"{'Reliability & Ordering':<26} | {'Guaranteed':<16} | {'Best-Effort':<16}")
    print(f"{'Transport Acknowledgment':<26} | {'Yes (ACK)':<16} | {'None':<16}")
    print(f"{'Header Overhead':<26} | {'20 - 60 Bytes':<16} | {'8 Bytes':<16}")
    print("=" * 64)
