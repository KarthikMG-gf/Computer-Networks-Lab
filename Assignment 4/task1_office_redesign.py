"""Task 1: Office bus-network problems and extended-star redesign."""

def file_transfer_time_mb(size_mb, bandwidth_mbps, users=1):
    """Ideal transfer time when users share one link equally."""
    per_user_mbps = bandwidth_mbps / users
    return (size_mb * 8) / per_user_mbps

def show_comparison():
    file_mb = 10
    users_month_end = 6
    users_all = 30

    print("TASK 1 - OFFICE NETWORK COMPARISON")
    print("-" * 48)
    print("Existing coaxial bus + hub (10 Mbps shared)")
    print(f"  Share for 30 active users: {10/users_all:.2f} Mbps each")
    print(f"  Share for 6 active users : {10/users_month_end:.2f} Mbps each")
    print(f"  Ideal 10 MB save (6 users): "
          f"{file_transfer_time_mb(file_mb, 10, users_month_end):.1f} seconds")

    print("\nRedesigned switched star (1 Gbps access ports)")
    print("  Each PC has a dedicated 1 Gbps full-duplex switch port.")
    print(f"  Ideal 10 MB save (6 users, shared 1 Gbps server link): "
          f"{file_transfer_time_mb(file_mb, 1000, users_month_end):.2f} seconds")
    print(f"  Ideal 10 MB save (30 users, shared 1 Gbps server link): "
          f"{file_transfer_time_mb(file_mb, 1000, users_all):.2f} seconds")

    print("\nRecommended logical design:")
    print("  Floor-1 core switch -> Floor-2 access switch (2 x 1 Gbps)")
    print("  PCs -> dedicated Cat6 links; server/printer -> core switch")
    print("  VLAN 10 Staff, VLAN 20 Server/Printer, VLAN 30 Guest")
    print("  Business firewall/router with primary WAN + 4G backup")

if __name__ == "__main__":
    show_comparison()
