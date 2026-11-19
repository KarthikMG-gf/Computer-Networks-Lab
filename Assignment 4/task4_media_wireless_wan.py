"""Task 4: ALOHA, CSMA/CD, Wi-Fi capacity and ATM calculations."""
import math

def aloha():
    pure = 1 / (2 * math.e)
    slotted = 1 / math.e
    print("ALOHA maximum throughput")
    print(f"  Pure ALOHA   : {pure:.3%} = {10*pure:.2f} Mbps on 10 Mbps")
    print(f"  Slotted ALOHA: {slotted:.3%} = {10*slotted:.2f} Mbps on 10 Mbps")

def csma_cd():
    distance_m = 2500
    signal_speed = 2e8
    data_rate = 10e6
    one_way = distance_m / signal_speed
    round_trip = 2 * one_way
    min_bits = data_rate * round_trip
    print("\nCSMA/CD propagation and minimum frame")
    print(f"  One-way propagation: {one_way*1e6:.2f} microseconds")
    print(f"  Round-trip delay   : {round_trip*1e6:.2f} microseconds")
    print(f"  Calculated minimum : {min_bits:.0f} bits ({min_bits/8:.2f} bytes)")

def wifi_plan():
    phones, clients_per_ap = 300, 40
    aps = math.ceil(phones / clients_per_ap)
    five_ghz = round(phones * 0.80)
    two_four = phones - five_ghz
    print("\nWi-Fi 6 waiting-hall capacity")
    print(f"  Access points required: {aps}")
    print(f"  5 GHz phones: {five_ghz}; per AP: {five_ghz/aps:.1f}")
    print(f"  2.4 GHz phones: {two_four}; if 4 AP radios used: {two_four/4:.1f} each")
    print("  Suggested 2.4 GHz channels: 1, 6, 11 (20 MHz)")
    print("  Suggested 5 GHz channels: 36, 40, 44, 48, 149, 153, 157, 161")

def atm():
    cell_bytes, header_bytes, payload_bytes = 53, 5, 48
    overhead = header_bytes / cell_bytes
    payload_eff = payload_bytes / cell_bytes
    rate = 155.52e6
    cell_time = cell_bytes * 8 / rate
    print("\nATM cell calculation")
    print(f"  Header overhead: {overhead:.2%}")
    print(f"  Payload efficiency: {payload_eff:.2%}")
    print(f"  Cell transmission time at 155.52 Mbps: {cell_time*1e6:.2f} microseconds")

if __name__ == "__main__":
    aloha()
    csma_cd()
    wifi_plan()
    atm()
