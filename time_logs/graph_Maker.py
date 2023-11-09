import matplotlib.pyplot as plt
import numpy as np

# Read the time entries from the file
with open("windows_program_log.txt", "r") as file:
    time_entries = [float(line.strip()) for line in file.readlines()]

# Calculate statistics
average_time = np.mean(time_entries)
std_deviation = np.std(time_entries)

# Define the dynamic threshold as a multiple of the standard deviation
threshold_multiplier = 2  # You can adjust this multiplier as needed
dynamic_threshold = average_time + threshold_multiplier * std_deviation

# Filter out outliers using the dynamic threshold
time_entries = [entry for entry in time_entries if entry <= dynamic_threshold]

# Limit the graph to show only the most recent 100 entries
entries = 100
time_entries = time_entries[-entries:]

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
plt.axhline(
    dynamic_threshold,
    color="red",
    linestyle="--",
    label=f"Dynamic Threshold ({threshold_multiplier} Std Dev)",
)
plt.title("Windows Program Log (Outliers Ignored, Most Recent 100 Entries)")
plt.xlabel("Entry Number")
plt.ylabel("Time (seconds)")
plt.legend()

# Save the plot as a PNG file
plt.savefig(f"windows_program_log_filtered{entries}.png")

# Show the plot (optional)
plt.show()

# Display statistics
print("Statistics for the most recent 100 time entries:")
print(f"Average: {average_time:.2f} seconds")
print(
    f"Dynamic Threshold ({threshold_multiplier} Std Dev): {dynamic_threshold:.2f} seconds"
)
