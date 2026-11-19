"""Task A4: Stateless packet filter: the first matching rule decides (like iptables)."""

RULES = [  # (action, protocol, destination port or None for any, source prefix or None)
    ("allow", "tcp", 443, None),
    ("allow", "tcp", 22, "10.1."),
    ("deny", "tcp", 22, None),
    ("allow", "udp", 53, None),
]
DEFAULT = "deny"

def decide(proto, port, src):
    for action, p, dport, prefix in RULES:
        # TODO 1: Completed rule matching condition
        if p == proto and (dport is None or dport == port) and (prefix is None or src.startswith(prefix)):
            return action
    return DEFAULT

if __name__ == "__main__":
    packets = [
        ("tcp", 443, "49.37.2.8"),
        ("tcp", 22, "10.1.4.20"),
        ("tcp", 22, "49.37.2.8"),
        ("udp", 53, "10.1.4.20"),
        ("tcp", 80, "49.37.2.8"),
        ("icmp", None, "49.37.2.8"),
    ]
    print("--- Original Corrected Rule Order ---")
    for pk in packets:
        print(f"{pk[0]:<5} {str(pk[1]):<5} from {pk[2]:<10} -> {decide(*pk)}")

    # Swap 2nd and 3rd rules to demonstrate rule shadowing
    RULES[1], RULES[2] = RULES[2], RULES[1]
    print("\n--- After Swapping Rules 2 and 3 (Shadowing Effect) ---")
    for pk in packets:
        print(f"{pk[0]:<5} {str(pk[1]):<5} from {pk[2]:<10} -> {decide(*pk)}")
