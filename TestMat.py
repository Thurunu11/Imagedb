import serial
import numpy as np

ser = serial.Serial('COM8', 115200)
ser.flushInput()
ser.flushOutput()

# Define the 24x32 array
array_rows, array_cols = (24, 32)
data_array = np.zeros((array_rows, array_cols))

# Keep track of the current row being written to the array
current_row = 0

# Skip the first image
first_image_skipped = False

while True:
    try:

        # Wait for data to be available on the serial port
        while ser.in_waiting == 0:
            pass

        # Read a line of data from the serial port
        line = ser.readline().decode('utf-8').strip()

        # Skip the first image
        if not first_image_skipped:
            if line == '':
                first_image_skipped = True
            continue

        # Parse the data from the line
        values = line.split(',')
        if len(values) != array_cols:
            continue

        # Convert the values to floats and write them to the array
        try:
            data_row = np.array([float(val) for val in values])
            data_array[current_row, :] = data_row
            current_row += 1
            if current_row >= array_rows:
                # Once we have read all the rows, print the 2D numpy array
                A = (','.join([','.join([str(val) for val in row]) for row in data_array]))
                current_row = 0
                print(A)
        except ValueError:
            continue

    except Exception as e:
        print(str(e))
