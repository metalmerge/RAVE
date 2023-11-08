import matplotlib.pyplot as plt
import numpy as np

# Define a threshold to ignore massive outliers
outlier_threshold = 60.0  # You can adjust this threshold as needed

# Read the time entries from the file and filter out outliers
with open("windows_program_log.txt", "r") as file:
    time_entries = [
        float(line.strip())
        for line in file.readlines()
        if float(line.strip()) <= outlier_threshold
    ]

# Limit the graph to show only the most recent 100 entries
time_entries = time_entries[-100:]

# Calculate statistics
average_time = np.mean(time_entries)
median_time = np.median(time_entries)
std_deviation = np.std(time_entries)

# Create a plot
plt.figure(figsize=(10, 6))  # You can adjust the figure size as needed

# Add a moving average trend line (e.g., 5-point moving average)
window_size = 5
moving_average = np.convolve(
    time_entries, np.ones(window_size) / window_size, mode="valid"
)
moving_average = np.pad(
    moving_average, (window_size - 1, 0), "constant", constant_values=np.nan
)

plt.plot(time_entries, marker="o", linestyle="-", label="Time Entries")
plt.plot(moving_average, linestyle="--", label=f"{window_size}-Point Moving Average")
plt.title("Windows Program Log (Outliers Ignored, Most Recent 100 Entries)")
plt.xlabel("Entry Number")
plt.ylabel("Time (seconds)")
plt.legend()

# Save the plot as a PNG file
plt.savefig("windows_program_log_filtered.png")

# Show the plot (optional)
plt.show()

# Display statistics
print("Statistics for the most recent 100 time entries:")
print(f"Average: {average_time:.2f} seconds")
print(f"Median: {median_time:.2f} seconds")
print(f"Standard Deviation: {std_deviation:.2f} seconds")
