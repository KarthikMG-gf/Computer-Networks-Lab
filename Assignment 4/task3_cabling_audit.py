"""Task 3: Cable-length audit, T568B reference and bill-of-material calculations."""

T568B = [
    "white-orange", "orange", "white-green", "blue",
    "white-blue", "green", "white-brown", "brown"
]
T568A = [
    "white-green", "green", "white-orange", "blue",
    "white-blue", "orange", "white-brown", "brown"
]

def audit_run(name, length_m, permanent_limit=90, channel_limit=100):
    verdict = "PASS" if length_m <= permanent_limit else "FAIL"
    print(f"{name:22} {length_m:6.1f} m  {verdict}")
    if length_m > permanent_limit:
        print(" " * 24 + "Permanent link exceeds 90 m; redesign or use fibre.")
    elif length_m > 55:
        print(" " * 24 + "Suitable for 1G; use Cat6A if 10G is required.")
    return verdict == "PASS"

def boxes_needed(total_m, box_length=305):
    import math
    return math.ceil(total_m / box_length)

def main():
    print("TASK 3 - CABLING LENGTH AUDIT")
    audit_run("Consulting-room longest", 80)
    audit_run("Pharmacy", 96)
    audit_run("Waiting-hall AP", 60)
    audit_run("Inter-building link", 420)

    pharmacy_channel = 96 + 2 * 3
    print(f"\nPharmacy channel incl. patch cords: {pharmacy_channel} m")
    print("T568B pin order:")
    for pin, colour in enumerate(T568B, start=1):
        print(f"  Pin {pin}: {colour}")

    print("\nExample cable quantities (including 10% allowance):")
    cat6_m = (2300 + 240) * 1.10
    cat6a_m = (8 * 60) * 1.10
    print(f"  Cat6:  {cat6_m:.0f} m -> {boxes_needed(cat6_m)} boxes of 305 m")
    print(f"  Cat6A: {cat6a_m:.0f} m -> {boxes_needed(cat6a_m)} boxes of 305 m")
    print("\nT568A-to-T568B is a crossover wiring pattern; use T568B at both")
    print("ends as the standard straight-through patch cable.")

if __name__ == "__main__":
    main()
