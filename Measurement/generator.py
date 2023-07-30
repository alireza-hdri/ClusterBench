# Define disk file path
disk_file_path = "./disks.txt"
metrics_file_path = "./metric.txt"

def measurement_generator(input_value):
    match input_value:
        case "1":
            print("You chose ops.")
            with open(disk_file_path, "r") as file:
                disks = file.readlines()
                for line_num, disk in enumerate(disks, start=1):
                    with open(metrics_file_path, "a") as metrics_file:
                        metrics_file.write(f"netdata.disk_ops.{disk.strip()}.reads\n")
                        metrics_file.write(f"netdata.disk_ops.{disk.strip()}.write\n")
                    print(f"Line {line_num}: {disk.strip()}")
            print(f"Total lines: {len(disks)}")
        case "2":
            print("You chose option 2.")
            # Implement functionality for option 2
        case "3":
            print("You chose option 3.")
            # Implement functionality for option 3
        case "exit":  # Added "exit" as an exit condition
            print("Exiting the program.")
        case _:
            print("Invalid option.")

# Example usage with loop:
while True:
    print('''
      Which want to generate ? 
      
      1) OPS (read and write)
      2) Option 2
      3) Option 3
      Enter "exit" to exit.''')
    user_input = input("\n Enter your choice: ").lower()  # Convert input to lowercase for case-insensitivity

    if user_input == "exit":
        break  # Exit the loop if user enters "exit"
    
    measurement_generator(user_input)
