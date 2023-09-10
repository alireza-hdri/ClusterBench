import datetime
import os
import subprocess
import argparse
import calendar
import sys
import json
import time

# Specify address to address.json file
influxdb_conf_file_path = "./../conf/Software/InfluxdbConfig.json"

# Load the JSON data from the file and define adresses as a variable 
with open(influxdb_conf_file_path, 'r') as file:
    json_data = json.load(file)
Primary_influxdb_in_container_address = json_data['Main_influxdb_in_container_address']
Primary_influxdb_address_in_host = json_data['Main_influxdb_address_in_host']
Secondary_influxdb_address_in_host = json_data['Backup_influxdb_address_in_host']
Primary_influxdb_container_name = json_data['Main_influxdb_container_name']
Secondary_influxdb_container_name = json_data['Backup_influxdb_container_name']
Time_add_to_end_of_test = json_data['Time_add_to_end_of_test']
Time_reduce_from_first_of_test = json_data['Time_reduce_from_first_of_test']
Main_influxdb_DB_name = json_data['Main_influxdb_DB_name']

# Process given Test name as an arqument
argParser = argparse.ArgumentParser()
argParser.add_argument("-t", "--testname", help="Test Name (Directory in Result/)")
args = argParser.parse_args()
testDirectory = args.testname
global testDirectory2
testDirectory2 = args.testname
input_file = "./../result/"+testDirectory+"/time"

#time defenition
gmt_offset_seconds = 3 * 3600 + 30 * 60

# Add 1-minute delay
#time.sleep(60)

print(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* START OF BACKUP FOR\033[92m {testDirectory} \033[0m*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

def read_values_from_file(file_path):
    values = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            values.extend(line.strip().split(","))
    return values

def process_input_file(file_path_input):
    # set config time in seconds manually
    variable_offset_seconds = 5 * 60  # 5min

    with open(file_path_input, "r") as f:
        lines = f.readlines()
        for line in lines:
            
            # Split given time
            start_datetime_str, end_datetime_str = line.strip().split(",")
            
            # Convert start and end datetime strings to datetime objects
            start_datetime = datetime.datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.datetime.strptime(end_datetime_str, "%Y-%m-%d %H:%M:%S")
            
            # Reduce the GMT+03:30 offset to both datetime objects
            start_datetime_utc = start_datetime - datetime.timedelta(seconds=gmt_offset_seconds)
            end_datetime_utc = end_datetime - datetime.timedelta(seconds=gmt_offset_seconds)

            # define variables
            backup_start_datetime = start_datetime
            backup_end_datetime = end_datetime

            # Add/reduce the specified number of seconds to both datetime objects
            backup_start_datetime -= datetime.timedelta(seconds=Time_reduce_from_first_of_test)
            backup_end_datetime += datetime.timedelta(seconds=Time_add_to_end_of_test)

            # Convert the UTC datetime objects back to strings
            start_datetime_utc_str = start_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")
            end_datetime_utc_str = end_datetime_utc.strftime("%Y-%m-%d %H:%M:%S")

            # creating backup time format
            backup_start_time , backup_start_date = backup_start_datetime.strip().split(" ")
            start_time_backup = backup_start_date+"T"+backup_start_time+"Z"
            print("start_time_backup : ", start_time_backup)
            backup_end_time , backup_end_date = backup_end_datetime.strip().split(" ")
            end_time_backup = backup_end_date+"T"+backup_end_time+"Z"
            print("end_time_backup : ", end_time_backup)



            # Create dir name


            # Perform backup using influxd backup command
            backup_command = f"docker exec -it {Primary_influxdb_container_name} influxd backup -portable -db {Main_influxdb_DB_name} -start {start_time_backup} -end {end_time_backup} {Primary_influxdb_in_container_address}/backup > /dev/null "
            backup_process = subprocess.run(backup_command, shell=True)
            exit_code = backup_process.returncode
            if exit_code == 0:
                print("\033[92mBackup successful.\033[0m")
            else:
                print("\033[91mBackup failed.\033[0m")
                sys.exit(1)
            print()

            # Tar backup files and delete extra files
            tar_command = f"tar -cf {Primary_influxdb_address_in_host}/{backup_dir_name}/backup.tar.gz -C {Primary_influxdb_address_in_host}/{backup_dir_name}/backup . > /dev/null 2>&1"
            tar_process = subprocess.run(tar_command, shell=True)
            exit_code = tar_process.returncode
            if exit_code == 0:
                print("\033[92mTar successful.\033[0m")
                print()
            else:
                print("\033[91mTar failed.\033[0m")
                sys.exit(1)
                print()

            # Delete backup directory files
            del_command = f"rm -rf {Primary_influxdb_address_in_host}/{backup_dir_name}/backup/*"
            del_process = subprocess.run(del_command , shell=True)

            # Make info directory and move all into influxdb2 mount points
            os.makedirs(f"{Primary_influxdb_address_in_host}/{backup_dir_name}/info", exist_ok=True)
            cp_command = f"cp -r ./../result/{testDirectory}/* {Primary_influxdb_address_in_host}/{backup_dir_name}/info/"
            cp_process = subprocess.run(cp_command, shell=True)

	        #MV BACKUP.TAR.GZ TO influxdb2 and delete original file
            os.makedirs(Secondary_influxdb_address_in_host, exist_ok=True)
            mv_command = f"mv -f {Primary_influxdb_address_in_host}/*  {Secondary_influxdb_address_in_host}/"
            mv_process = subprocess.run(mv_command, shell=True)
            exit_code = mv_process.returncode
            if exit_code == 0:
                print(f"\033[92mFiles moved to {Secondary_influxdb_container_name} location successfully.\033[0m")
            else:
                print("\033[91mMoving files failed.\033[0m")
                sys.exit(1)
                print()

process_input_file(input_file)
print(f"*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* END OF BACKUP FOR\033[92m {testDirectory} \033[0m*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
