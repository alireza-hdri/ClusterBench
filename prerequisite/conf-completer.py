import os
import subprocess
import json

# Insert influxdb container names from user input
main_influxdb_container_name = input("Please enter your main InfluxDB container name (Default: influxdb): ")
if main_influxdb_container_name == "":
    main_influxdb_container_name = "influxdb"

Backup_influxdb_container_name = input("Please enter your main InfluxDB container name (Default: influxdb2): ")
if Backup_influxdb_container_name == "":
    Backup_influxdb_container_name = "influxdb2"

# Run docker command for main and backup influxdb
main_mount_point_command = f'docker inspect -f "{{{{range .Mounts}}}}{{{{if eq .Mode \\"rw\\"}}}}{{{{.Source}}}} {{{{.Destination}}}}{{{{end}}}}{{{{end}}}}" {main_influxdb_container_name}'
main_mount_point_process = subprocess.run(main_mount_point_command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

backup_mount_point_command = f'docker inspect -f "{{{{range .Mounts}}}}{{{{if eq .Mode \\"rw\\"}}}}{{{{.Source}}}} {{{{.Destination}}}}{{{{end}}}}{{{{end}}}}" {Backup_influxdb_container_name}'
backup_mount_point_process = subprocess.run(main_mount_point_command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

# Extracting and splitting the output for both containers
main_mount_point = main_mount_point_process.stdout.strip()
main_in_host_address, main_in_container_address = main_mount_point.strip().split(" ")

backup_mount_point = backup_mount_point_process.stdout.strip()
backup_in_host_address, backup_in_container_address = backup_mount_point.strip().split(" ")

# Find RP name
rp_finder_command = f"curl -G \"http://localhost:8086/query?db=opentsdb&pretty=true\" --data-urlencode \"q=SHOW RETENTION POLICIES\""
rp_finder_process = subprocess.run(rp_finder_command,shell=True, stdout=subprocess.PIPE, universal_newlines=True)
print(rp_finder_process.stdout)

# Load existing JSON
with open("data.json", "r") as json_file:
    existing_json = json.load(json_file)

# Add addresses to the existing JSON
existing_json["Main_influxdb_address_in_host"] = main_in_host_address
existing_json["Main_influxdb_in_container_address"] = main_in_container_address
existing_json["Backup_influxdb_address_in_host"] = backup_in_host_address
existing_json["Backup_influxdb_in_container_address"] = backup_in_container_address

# Save back the modified JSON
with open("data.json", "w") as json_file:
    json.dump(existing_json, json_file, indent=4)

print("Addresses added to JSON file.")
