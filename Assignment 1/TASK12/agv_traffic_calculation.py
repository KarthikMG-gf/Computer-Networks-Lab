"""
Task 12 - AGV Traffic Calculation
Run: python agv_traffic_calculation.py

IMPORTANT:
The packet size, message rate, and AGV count below are working assumptions.
Replace them with the values specified in your assignment or confirmed by
your project requirements before submitting.
"""

# Assumptions (edit these when confirmed)
packet_size_bytes = 500       # bytes per AGV message
messages_per_second = 20     # messages sent per second by each AGV
number_of_agvs = 10          # total number of AGVs
capacity_margin = 1.5        # 50% additional capacity headroom

# Traffic calculation
traffic_per_agv_bps = (
    packet_size_bytes * 8 * messages_per_second
)
total_traffic_bps = traffic_per_agv_bps * number_of_agvs

traffic_per_agv_mbps = traffic_per_agv_bps / 1_000_000
total_traffic_mbps = total_traffic_bps / 1_000_000
recommended_capacity_mbps = total_traffic_mbps * capacity_margin

print("AGV Traffic Calculation")
print("-----------------------")
print(f"Packet size per message : {packet_size_bytes} bytes")
print(f"Message rate per AGV    : {messages_per_second} messages/second")
print(f"Number of AGVs          : {number_of_agvs}")
print(f"Traffic per AGV         : {traffic_per_agv_mbps:.3f} Mbps")
print(f"Total AGV traffic       : {total_traffic_mbps:.3f} Mbps")
print(
    f"Recommended capacity   : >= {recommended_capacity_mbps:.3f} Mbps "
    f"({capacity_margin:.1f}x headroom)"
)

print("\nNote: This is a theoretical traffic estimate, not a measured 5G test.")
print("Validate latency, jitter, packet loss, and throughput using an actual")
print("5G testbed or a clearly identified simulation before reporting results.")
