"""AGV handover and sensor-capacity calculations for Task 5."""

route_m = 1200
agv_speed_mps = 2

wifi_spacing_m = 30
wifi_handover_s = 0.150
fiveg_cell_m = 300
fiveg_handover_s = 0.020

# Assuming the route starts at the beginning of the first coverage area
# and counts transitions between adjacent coverage areas.
wifi_areas = route_m / wifi_spacing_m
fiveg_areas = route_m / fiveg_cell_m
wifi_handovers = int(wifi_areas) - 1
fiveg_handovers = int(fiveg_areas) - 1

wifi_unreachable = wifi_handovers * wifi_handover_s
fiveg_unreachable = fiveg_handovers * fiveg_handover_s
trip_duration = route_m / agv_speed_mps

sensor_count = 600
bytes_per_sensor_second = 50
sensor_total_bps = sensor_count * bytes_per_sensor_second * 8
lora_capacity_bps = 5000

print("TASK 5 - AGV HANDOVER")
print(f"Trip duration: {trip_duration:.1f} seconds")
print(f"Wi-Fi handovers: {wifi_handovers}")
print(f"Wi-Fi unreachable time: {wifi_unreachable:.3f} seconds")
print(f"5G handovers: {fiveg_handovers}")
print(f"5G unreachable time: {fiveg_unreachable:.3f} seconds")

print("\nLORAWAN SENSOR CAPACITY CHECK")
print(f"600 sensors aggregate: {sensor_total_bps / 1000:.1f} kbps")
print(f"Approximate gateway capacity: {lora_capacity_bps / 1000:.1f} kbps")
print("Fits:", sensor_total_bps <= lora_capacity_bps)
