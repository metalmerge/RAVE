import matplotlib.pyplot as plt
import numpy as np

# Read data from the file
file_path = "time_logs/windows_program_log.txt"
with open(file_path, "r") as file:
    # Read lines and convert data to float
    data = [float(line.strip()) for line in file.readlines()]

# Convert data to NumPy array
data_array = np.array(data)

# Calculate mean, median, and standard deviation
std_dev = np.std(data_array)
mean = np.mean(data_array)

two_std = std_dev * 1
filtered_data = data_array[abs(data_array - mean) < two_std]
median = np.median(filtered_data)

window = 86
moving_avg = np.convolve(filtered_data, np.ones(window) / window, mode="valid")

# Sort data and get the lowest value
lowest_value = np.min(filtered_data)

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
plt.axhline(y=median, color="purple", linestyle="--", label=f"Median: {median:.2f}")
# plt.axhline(y=mean, color="yellow", linestyle="--", label=f"Mean: {mean:.2f}")
plt.axhline(y=mean + two_std, color="orange", linestyle="--", label="+1 SD")
# plt.scatter(
#     np.where(filtered_data == lowest_value),
#     lowest_value,
#     color="green",
#     label="Lowest Value",
# )
plt.xlabel("Index")
plt.ylabel("Value")
plt.title("Data with Moving Average and Outliers Removed")
plt.legend()
plt.grid(True)
plt.savefig(f"time_logs/graphImages/program_time_trials{data_array.size}.png")
plt.show()

print(f"Mean: {mean:.2f}")
print(f"Median: {median:.2f}")
print(f"Standard Deviation: {std_dev:.2f}")
print(f"Lowest Value: {lowest_value:.2f}")
print(moving_avg[-1])
