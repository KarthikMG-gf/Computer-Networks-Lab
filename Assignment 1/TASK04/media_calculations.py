"""Nyquist and Shannon capacity calculations."""
import math


def nyquist(bandwidth_hz, levels):
    return 2 * bandwidth_hz * math.log2(levels)


def shannon(bandwidth_hz, snr_db):
    snr_ratio = 10 ** (snr_db / 10)
    return bandwidth_hz * math.log2(1 + snr_ratio)


media = [
    ("Telephone line", 3100, 30),
    ("Cat6 pair", 250e6, 40),
    ("Wi-Fi 6 channel", 160e6, 25)
]

for name, bandwidth, snr in media:
    print(f"{name:<18} Shannon limit {shannon(bandwidth, snr) / 1e6:10.2f} Mbps")

print(f"Nyquist, 3,100 Hz with 4 levels: {nyquist(3100, 4) / 1e3:.1f} kbps")

print("\nWelding-area cable at 15 dB:")
print(f"{shannon(250e6, 15) / 1e6:.2f} Mbps")

print("\nWi-Fi 6, 160 MHz, welding-area SNR 15 dB:")
print(f"{shannon(160e6, 15) / 1e6:.2f} Mbps")

# SNR required for 56 kbps over a 3,100 Hz telephone channel
required_snr_ratio = 2 ** (56000 / 3100) - 1
required_snr_db = 10 * math.log10(required_snr_ratio)
print(f"\nSNR required for 56 kbps: {required_snr_db:.2f} dB")
