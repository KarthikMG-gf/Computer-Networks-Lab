"""Stop-and-wait and sliding-window utilisation calculations."""


def utilisation(frame_bits, rate_bps, distance_m, window, speed=2e8):
    tx = frame_bits / rate_bps
    prop = distance_m / speed
    a = prop / tx
    u = min(1.0, window / (1 + 2 * a))
    return u, a


links = [
    ("Campus LAN, 200 m, 1 Gbps", 1e9, 200),
    ("City fibre, 50 km, 1 Gbps", 1e9, 50_000),
    ("Satellite, 36,000 km, 10 Mbps", 10e6, 36_000_000)
]

for name, rate, distance in links:
    u1, a = utilisation(12_000, rate, distance, 1)
    u7, _ = utilisation(12_000, rate, distance, 7)
    u127, _ = utilisation(12_000, rate, distance, 127)
    print(f"{name:<31} a = {a:7.2f} stop-and-wait {u1:6.1%} "
          f"W=7 {u7:6.1%} W=127 {u127:6.1%}")

# Assignment head-office link: 400 km fibre, 1 Gbps, 1500-byte frames
frame_bits = 1500 * 8
rate = 1e9
distance = 400_000
tx = frame_bits / rate
prop = distance / 2e8
a = prop / tx
required_window = int((1 + 2 * a) // 1) + 1
u64, _ = utilisation(frame_bits, rate, distance, 64)
throughput64 = u64 * rate

print("\n400 km head-office link")
print(f"Transmission time: {tx * 1e6:.2f} microseconds")
print(f"One-way propagation time: {prop * 1000:.2f} ms")
print(f"a = {a:.2f}")
print(f"Stop-and-wait utilisation: {1 / (1 + 2*a):.4%}")
print(f"Minimum full-utilisation window: {required_window}")
print(f"Go-Back-N sequence bits: {(required_window + 1 - 1).bit_length()}")
print(f"Selective Repeat sequence bits: {(2 * required_window - 1).bit_length()}")
print(f"Selective Repeat W=64 utilisation: {u64:.2%}")
print(f"Selective Repeat W=64 throughput: {throughput64 / 1e6:.2f} Mbps")
print(f"Selective Repeat W=64 receiver data buffer: {64 * 1500} bytes")
