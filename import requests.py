import requests
import os
import folium
import time

# ESP32 Access Point IP
esp32_ip = "Your_IP_Address"

# List to store multiple GPS points
gps_points = []

# Number of samples to collect (you can change this)
NUM_POINTS = 5
SAMPLE_INTERVAL_SEC = 5  # fetch every 5 seconds

for i in range(NUM_POINTS):
    try:
        response = requests.get(esp32_ip, timeout=5)
        if response.status_code == 200:
            data = response.text.strip()
            print(f"[{i+1}] Raw: {data}")

            # Parse the Latitude and Longitude
            lines = data.split("\n")
            lat = float(lines[0].split(":")[1].strip())
            lng = float(lines[1].split(":")[1].strip())

            gps_points.append((lat, lng))
            print(f"Point added: {lat}, {lng}")
        else:
            print("ESP32 response failed with status code:", response.status_code)
    except Exception as e:
        print("Error:", e)
    
    time.sleep(SAMPLE_INTERVAL_SEC)

# === Generate the map ===
if gps_points:
    gps_map = folium.Map(location=gps_points[0], zoom_start=16)

    # Add a marker for each point
    for idx, (lat, lng) in enumerate(gps_points, start=1):
        folium.Marker(
            [lat, lng],
            popup=f"Point {idx}",
            tooltip=f"GPS {idx}",
            icon=folium.Icon(color="blue")
        ).add_to(gps_map)

    # Optional: draw path between them
    folium.PolyLine(gps_points, color="red", weight=2.5).add_to(gps_map)

    # Save and show map
    file_name = "multi_gps_map.html"
    gps_map.save(file_name)
    os.system(f'start {os.path.abspath(file_name)}')
else:
    print("No GPS points collected.")
