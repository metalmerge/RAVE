import matplotlib.pyplot as plt
import numpy as np

# Read data from the file
file_path = "windows_program_log.txt"
with open(file_path, "r") as file:
    # Read lines and convert data to float
    data = [float(line.strip()) for line in file.readlines()]

# Convert data to NumPy array
data_array = np.array(data)

# Calculate mean, median, and standard deviation
mean = np.mean(data_array)
std_dev = np.std(data_array)

two_std = 2 * std_dev
filtered_data = data_array[abs(data_array - mean) < two_std]
median = np.median(filtered_data)

# Calculate 10-point moving average
window = 100
moving_avg = np.convolve(filtered_data, np.ones(window) / window, mode="valid")

# Create a figure and plot the data
plt.figure(figsize=(8, 6))
plt.scatter(
    range(len(filtered_data)), filtered_data, color="red", label="Filtered Data"
)
plt.plot(
    range(window - 1, len(filtered_data)),
    moving_avg,
    color="blue",
    label="Moving Average",
)
# plt.axhline(y=mean, color="green", linestyle="--", label=f"Mean: {mean:.2f}")
plt.axhline(y=median, color="purple", linestyle="--", label=f"Median: {median:.2f}")
plt.axhline(y=mean + two_std, color="orange", linestyle="--", label="+2 SD")
plt.xlabel("Index")
plt.ylabel("Value")
plt.title("Data with Moving Average and Outliers Removed")
plt.legend()
plt.savefig(f"program_time_trials{data_array.size}.png")
plt.show()

# Display the mean, median, and standard deviation
print(f"Mean: {mean:.2f}")
print(f"Median: {median:.2f}")
print(f"Standard Deviation: {std_dev:.2f}")
