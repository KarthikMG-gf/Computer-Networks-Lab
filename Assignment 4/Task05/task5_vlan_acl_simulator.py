"""Task 5: Simulate VLAN segmentation and guest ACL policy."""

NETWORKS = {
    "Office": "192.168.10.0/24",
    "CCTV": "192.168.20.0/24",
    "Guest": "192.168.30.0/24",
}

def allowed(source_vlan, destination_ip):
    import ipaddress
    dst = ipaddress.ip_address(destination_ip)
    if source_vlan == "Guest" and dst.is_private:
        return False
    return True

def test(source_vlan, destination_ip):
    result = "ALLOW" if allowed(source_vlan, destination_ip) else "BLOCK"
    print(f"{source_vlan:8} -> {destination_ip:15} : {result}")

def main():
    print("VLAN membership")
    for vlan, subnet in NETWORKS.items():
        print(f"  VLAN {vlan:8} {subnet}")

    print("\nACL test cases")
    test("Office", "192.168.20.10")
    test("Office", "192.168.30.10")
    test("Guest", "192.168.10.10")
    test("Guest", "192.168.20.10")
    test("Guest", "203.0.113.10")

    print("\nCisco switch configuration reminder:")
    print("  VLAN 10 = Office; VLAN 20 = CCTV; VLAN 30 = Guest")
    print("  Access ports assigned to their VLAN; uplink trunk allows 10,20,30.")
    print("  Router subinterfaces use dot1Q tags and .1 gateway addresses.")

if __name__ == "__main__":
    main()
