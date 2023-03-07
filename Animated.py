import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ser = serial.Serial('COM8', 115200)
ser.flushInput()
ser.flushOutput()

# Initialize the array
line = ''

# Define the 24x32 array
array_rows, array_cols = (24, 32)
data_array = np.zeros((array_rows, array_cols))

# Keep track of the current row being written to the array
current_row = 0

# Skip the first image
first_image_skipped = False

# Create a figure and an axis for the heatmap
fig, ax = plt.subplots()

# Set the x and y labels and the title of the heatmap
ax.set_xlabel('Column')
ax.set_ylabel('Row')
ax.set_title('Data Array Heatmap')

# Create an empty heatmap using the imshow function
heatmap = ax.imshow(data_array, cmap='jet', animated=True)


# Define a function to update the heatmap at each animation frame
def update(frame):
    global data_array, current_row, first_image_skipped

    # Wait for data to be available on the serial port
    while ser.in_waiting == 0:
        pass

    # Read a line of data from the serial port
    line = ser.readline().decode('utf-8').strip()

    # Skip the first image
    if not first_image_skipped:
        if line == '':
            first_image_skipped = True
        return [heatmap]

    # Parse the data from the line
    values = line.split(',')
    if len(values) != array_cols:
        return [heatmap]

    # Convert the values to floats and write them to the array
    try:
        data_row = np.array([float(val) for val in values])
        data_array[current_row, :] = data_row
        current_row += 1
        if current_row >= array_rows:
            current_row = 0

        # Update the data in the heatmap
        heatmap.set_array(data_array)

    except ValueError:
        pass

    # Return the updated heatmap
    return [heatmap]


# Create the animation using the FuncAnimation function
animation = FuncAnimation(fig, update, frames=range(100), interval=100)

# Display the animation
plt.show()
