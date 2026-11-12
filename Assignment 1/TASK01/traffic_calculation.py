# Task 1: Smart manufacturing plant traffic sizing

robots = 40
sensors = 600
cameras = 24
office_users = 150

# Traffic in Mbps
robot_per_device = (200 * 8) / 0.002 / 1_000_000
sensor_per_device = (50 * 8) / 1_000_000
camera_per_device = 4
active_office_users = office_users * 0.10
office_per_active_user = 2

robot_total = robots * robot_per_device
sensor_total = sensors * sensor_per_device
camera_total = cameras * camera_per_device
office_total = active_office_users * office_per_active_user

one_line = robot_total + sensor_total + camera_total + office_total
eight_lines = one_line * 8

# Alternative: cameras record locally and transmit only 5% of the time
reduced_camera_total = camera_total * 0.05
alternative_line = robot_total + sensor_total + reduced_camera_total + office_total
alternative_plant = alternative_line * 8

print("TASK 1 - TRAFFIC SIZING")
print(f"Robot controllers : {robot_total:.2f} Mbps")
print(f"Vibration sensors : {sensor_total:.2f} Mbps")
print(f"CCTV cameras      : {camera_total:.2f} Mbps")
print(f"Office users      : {office_total:.2f} Mbps")
print(f"One production line: {one_line:.2f} Mbps")
print(f"Eight-line plant   : {eight_lines:.2f} Mbps")
print()
print("ALTERNATIVE: LOCAL CCTV RECORDING")
print(f"Reduced CCTV       : {reduced_camera_total:.2f} Mbps")
print(f"Alternative/line  : {alternative_line:.2f} Mbps")
print(f"Alternative/plant : {alternative_plant:.2f} Mbps")
print()
print("1 Gbps uplink original:", "INSUFFICIENT" if eight_lines > 1000 else "SUFFICIENT")
print("1 Gbps uplink alternative:", "INSUFFICIENT" if alternative_plant > 1000 else "SUFFICIENT")
