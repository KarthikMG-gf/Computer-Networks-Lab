"""Q4: Iterative DNS resolution through root, TLD and authoritative servers with TTL cache."""
import time

SERVERS = {
    "root": {"in.": "tld-in", "com.": "tld-com"},
    "tld-in": {"ac.in.": "ns-ac"},
    "tld-com": {"example.com.": "ns-example"},
    "ns-ac": {"simats.ac.in.": "ns-simats"},
    "ns-simats": {"results.simats.ac.in.": "10.20.30.40"},
    "ns-example": {"www.example.com.": "93.184.216.34"},
}

cache = {}  # Maps domain_name -> (ip_address, expiry_timestamp)

def resolve(name, ttl=300):
    now = time.time()
    if name in cache:
        ip, expires_at = cache[name]
        if now < expires_at:
            return ip, 0
        else:
            del cache[name]

    server, queries = "root", 0
    while True:
        queries += 1
        # TODO 1: Look in SERVERS[server] for the longest key that name ends with. If
        #   the value looks like an IP address (it contains a digit), cache it and
        #   return (ip, queries); otherwise continue with that server
        zone_table = SERVERS[server]
        longest_key = max((k for k in zone_table if name.endswith(k)), key=len)
        target = zone_table[longest_key]
        if any(ch.isdigit() for ch in target):
            cache[name] = (target, now + ttl)
            return target, queries
        server = target

if __name__ == "__main__":
    for n in ("results.simats.ac.in.", "www.example.com.", "results.simats.ac.in."):
        ip, q = resolve(n, ttl=300)
        print(f"{n:<24} {ip:<15} queries sent: {q}")
