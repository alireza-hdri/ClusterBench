import os
import subprocess
import json

influxdb_container_name = input("Please enter your main InfluxDB container name (Default: influxdb): ")
if influxdb_container_name == "":
    influxdb_container_name = "influxdb"

# Docker command
main_mount_point_command = f'docker inspect -f "{{{{range .Mounts}}}}{{{{if eq .Mode \\"rw\\"}}}}{{{{.Source}}}} {{{{.Destination}}}}{{{{end}}}}{{{{end}}}}" {influxdb_container_name}'
main_mount_point_process = subprocess.run(main_mount_point_command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

# Extracting and splitting the output
main_mount_point = main_mount_point_process.stdout.strip()
first_address, second_address = main_mount_point.strip().split(" ")

# Load existing JSON
with open("data.json", "r") as json_file:
    existing_json = json.load(json_file)

# Add addresses to the existing JSON
existing_json["first_address"] = first_address
existing_json["second_address"] = second_address

# Save back the modified JSON
with open("data.json", "w") as json_file:
    json.dump(existing_json, json_file, indent=4)

print("Addresses added to JSON.")
