import sys
import subprocess
import generate_xml
import os

script_path = './../../cli.sh'
arg1 = 'submit'

input_file = sys.argv[1]
default_file = sys.argv[2]
script_file = sys.argv[3]

temp_output_path = './temp_output'
temp_output_xml_path = './temp_output.xml'

input = open(input_file, "r")
lines = input.read().split('}')
workloads = len(lines)
workloads -= 1

workload_name = ""

# Example usage
path = '/path/to/folder'  # Replace with your desired path
filename = 'example.txt'  # Replace with the name of the file you want to check

check_file_exists(path, filename)


for workload_number in range(workloads):
    temp_output_file = temp_output_path + "_" + str(workload_number)
    temp_output_file_xml = temp_output_xml_path + "_" + str(workload_number)
    file = open(temp_output_file, "w")
    file.write(lines[workload_number])
    file.close()
    generate_xml.convert_input_to_xml(temp_output_file, default_file, temp_output_file_xml)
    file = open(temp_output_file, 'r')
    every_line = file.readlines()
    for l in every_line:
        if '{' in l:
            workload_name = l.split('{')[0].strip().rstrip()
    print(f"Workload: {workload_name} is running")
    arg2 = temp_output_file_xml
    # subprocess.call(["bash", script_path, arg1, arg2])
    result = subprocess.call(["bash", script_path, arg1, arg2])
    # while True:
    #     file_path = os.path.join(path, filename)  # Construct the absolute file path
    # if os.path.exists(file_path):
    #     print(f"The file '{filename}' exists in the path '{path}'.")
    #     return True
    # else:
    #     print(f"The file '{filename}' does not exist in the path '{path}'.")
    #     return False
    os.remove(temp_output_file) 
    os.remove(temp_output_file_xml)
    print("--------------------------------------")
