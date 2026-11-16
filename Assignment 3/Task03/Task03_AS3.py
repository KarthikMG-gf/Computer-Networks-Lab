"""Q3: Analytical and simulated page-load time calculator (1 HTML + 80 objects)."""
import math

def compute_http_times(num_objects=80, rtt_ms=50):
    total_files = 1 + num_objects
    t_non_persist_1 = total_files * 2 * rtt_ms
    t_persist_unpipelined = (1 + total_files) * rtt_ms
    t_persist_pipelined = 3 * rtt_ms
    rounds_6 = math.ceil(num_objects / 6)
    t_parallel_6 = (2 + 2 * rounds_6) * rtt_ms

    # Alternative: 8 bundles (1 HTML + 8 bundles = 9 files)
    t_bundled_non_persist = 9 * 2 * rtt_ms
    t_bundled_persist = (1 + 9) * rtt_ms

    print(f"RTT = {rtt_ms} ms | 1 HTML + {num_objects} objects:")
    print(f"  Non-persistent HTTP (1 conn)      : {t_non_persist_1} ms ({t_non_persist_1/1000:.2f} s)")
    print(f"  Persistent HTTP/1.1 (unpipelined) : {t_persist_unpipelined} ms ({t_persist_unpipelined/1000:.2f} s)")
    print(f"  Persistent HTTP/1.1 (pipelined)   : {t_persist_pipelined} ms ({t_persist_pipelined/1000:.2f} s)")
    print(f"  6 Parallel Non-persistent conns   : {t_parallel_6} ms ({t_parallel_6/1000:.2f} s)")
    print(f"  Alternative (8 Bundles, Non-Pers) : {t_bundled_non_persist} ms ({t_bundled_non_persist/1000:.2f} s)")
    print(f"  Alternative (8 Bundles, Persist)  : {t_bundled_persist} ms ({t_bundled_persist/1000:.2f} s)")

if __name__ == "__main__":
    compute_http_times(80, 50)
