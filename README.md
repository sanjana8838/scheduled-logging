# scheduled-logging
This is a Python script designed to connect to a Modbus TCP server, read various registers, and log the data into a CSV file at regular intervals. This script utilizes the PyModbus library for Modbus communication and the pandas library for data manipulation and storage.

## Features

- **Modbus Connection:** Connects to a Modbus TCP server with specified IP address and port.

- **Data Reading:** Reads multiple Modbus registers at regular intervals.

- **Data Logging:** Logs the read data into a CSV file, appending new rows for each reading.

- **Negative Value Handling:** Handles negative values from Modbus registers appropriately.

- **Timestamping:** Includes a timestamp for each data reading, capturing both Unix timestamp and human-readable timestamp.

- **Scheduler:** Utilizes the APScheduler library to schedule and execute the data reading and logging at defined intervals.

## Configuration

1. **Modbus Connection:**
   - Modify the `ModbusConnect` function to specify the IP address and port of your Modbus TCP server.

2. **Register Configuration:**
   - Adjust the register addresses in the `ReadRegister` function based on your Modbus device's register map.

3. **Logging Configuration:**
   - Configure the CSV file name and path in the `save_csv` function.

## Dependencies

- Python 3.x
- pandas library
- pymodbus library
- apscheduler library

## Getting Started

1. **Install Dependencies:**
   - Install the required dependencies using the following:
     ```
     pip install pandas pymodbus apscheduler
     ```

2. **Run the Script:**
   - Execute the script by running `python script_name.py` in your terminal.

3. **View Data:**
   - Open the generated CSV file to view the logged data.

## Notes

- The script uses a background scheduler to read and log data at regular intervals. Adjust the interval as needed.

- Ensure that the Modbus registers being read match the configuration of your Modbus device.

- Customize the CSV file naming and path according to your preferences.

## Author

Sanjana Ramesh
