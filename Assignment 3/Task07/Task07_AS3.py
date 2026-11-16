"""Q7: Telemedicine platform verification: throughput limit + multi-channel chat & file transfer."""
import hashlib
import os
import socket
import threading
import time

def tcp_window_throughput_limit(window_bytes=65535, rtt_sec=0.300, file_size_mb=15):
    bps = (window_bytes * 8) / rtt_sec
    mbps = bps / 1_000_000.0
    transfer_sec = (file_size_mb * 8 * 1_000_000) / bps
    print(f"64 KB Window @ 300 ms RTT -> Max Throughput: {mbps:.3f} Mbps")
    print(f"Minimum transfer time for {file_size_mb} MB X-Ray: {transfer_sec:.2f} seconds")

def run_telemedicine_demo():
    # Verify concurrent chat and X-ray binary transfer with SHA-256 integrity
    xray_data = os.urandom(256 * 1024)  # 256 KB test X-ray image
    expected_hash = hashlib.sha256(xray_data).hexdigest()

    file_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    file_srv.bind(("127.0.0.1", 0))
    file_srv.listen(1)

    chat_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_srv.bind(("127.0.0.1", 0))
    chat_srv.listen(1)

    def handle_xray():
        conn, _ = file_srv.accept()
        with conn:
            buf = bytearray()
            while True:
                chunk = conn.recv(8192)
                if not chunk:
                    break
                buf.extend(chunk)
            actual_hash = hashlib.sha256(buf).hexdigest()
            print(f"X-Ray Received: {len(buf)} bytes | SHA-256 Match: {actual_hash == expected_hash}")

    def handle_chat():
        conn, _ = chat_srv.accept()
        with conn:
            msg = conn.recv(1024).decode()
            conn.sendall(f"DOCTOR_ACK: {msg}".encode())

    t1 = threading.Thread(target=handle_xray)
    t2 = threading.Thread(target=handle_chat)
    t1.start()
    t2.start()

    start = time.perf_counter()
    fc = socket.create_connection(file_srv.getsockname())
    fc.sendall(xray_data)
    fc.close()

    cc = socket.create_connection(chat_srv.getsockname())
    cc.sendall(b"Patient SpO2 94%, uploading chest X-ray")
    reply = cc.recv(1024).decode()
    cc.close()

    t1.join()
    t2.join()
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    print(f"Chat Reply: '{reply}' | Concurrent Transfer Time: {elapsed_ms:.2f} ms")
    file_srv.close()
    chat_srv.close()

if __name__ == "__main__":
    tcp_window_throughput_limit()
    run_telemedicine_demo()
