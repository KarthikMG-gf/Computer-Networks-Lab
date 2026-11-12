"""Variable-length subnetting (VLSM) of 192.168.10.0/24 for a college campus."""
import math
import ipaddress

def to_int(ip):
    a, b, c, d = map(int, ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d

def to_ip(n):
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))

def vlsm(base, needs):
    addr = to_int(base)
    for name, hosts in sorted(needs, key=lambda x: -x[1]):
        # TODO 1: Find the smallest block that holds hosts + 2 addresses (a power of
        #   two), its prefix length 32 - log2(block), and print the network, prefix,
        #   first and last usable host and broadcast address. Then move addr to the next
        #   block
        block = 1 << math.ceil(math.log2(hosts + 2))
        prefix = 32 - int(math.log2(block))
        net_ip = to_ip(addr)
        first_ip = to_ip(addr + 1)
        last_ip = to_ip(addr + block - 2)
        bcast_ip = to_ip(addr + block - 1)
        print(f"{name:<13} {net_ip}/{prefix}  hosts {first_ip} - {last_ip}  bcast {bcast_ip}")
        addr += block
    return to_ip(addr)

needs = [("Labs", 100), ("Staff", 50), ("Library", 25), ("WAN link", 2)]
print("next free address:", vlsm("192.168.10.0", needs))

# Verification using Python's built-in ipaddress module & testing the 60-host Hostel trap
print("\n--- Verification with ipaddress module ---")
parent = ipaddress.IPv4Network("192.168.10.0/24")
allocated = [
    ipaddress.IPv4Network("192.168.10.0/25"),
    ipaddress.IPv4Network("192.168.10.128/26"),
    ipaddress.IPv4Network("192.168.10.192/27"),
    ipaddress.IPv4Network("192.168.10.224/30"),
]
for net in allocated:
    hosts = list(net.hosts())
    print(f"{net}: mask={net.netmask}, usable={len(hosts)} ({hosts[0]} - {hosts[-1]}), bcast={net.broadcast_address}")

# Check remaining free blocks inside 192.168.10.0/24
remaining = list(parent.address_exclude(allocated[0]))
for sub in allocated[1:]:
    next_rem = []
    for r in remaining:
        if sub.subnet_of(r):
            next_rem.extend(r.address_exclude(sub))
        else:
            next_rem.append(r)
    remaining = next_rem

print("Remaining free subnets in /24:", [str(r) for r in remaining])
print("Can a 60-host Hostel (/26 = 64 IPs) fit in remaining /24 space?", any(r.prefixlen <= 26 for r in remaining))
