import matplotlib.pyplot as plt
import numpy as np

# Read the time entries and interaction numbers from the file
with open("windows_program_log.txt", "r") as file:
    data = [line.strip().split("-") for line in file.readlines()]

# Separate data into lists
durations = [float(entry[0]) for entry in data]
interactions_numbers = [int(entry[1]) for entry in data]
date_times = [entry[2] for entry in data]

# Calculate statistics
average_time = np.mean(durations)
std_deviation = np.std(durations)

# Define the dynamic threshold as a multiple of the standard deviation
threshold_multiplier = 2  # You can adjust this multiplier as needed
dynamic_threshold = average_time + threshold_multiplier * std_deviation

# Filter out outliers using the dynamic threshold
filtered_data = [
    (d, i, dt)
    for d, i, dt in zip(durations, interactions_numbers, date_times)
    if d <= dynamic_threshold
]

# Separate filtered data into lists
filtered_durations, filtered_interactions_numbers, filtered_date_times = zip(
    *filtered_data
)

# Limit the graph to show only the most recent 100 entries
entries = 100
filtered_durations = filtered_durations[-entries:]
filtered_interactions_numbers = filtered_interactions_numbers[-entries:]
filtered_date_times = filtered_date_times[-entries:]

# Create a plot
plt.figure(figsize=(10, 6))  # You can adjust the figure size as needed

# Add a scatter plot with color-coded data points
plt.scatter(
    filtered_date_times,
    filtered_durations,
    c=filtered_interactions_numbers,
    cmap="viridis",
    marker="o",
    label="Time Entries",
)
plt.colorbar(label="Interactions Number")  # Add colorbar
plt.title("Windows Program Log (Outliers Ignored, Most Recent 100 Entries)")
plt.xlabel("Date and Time")
plt.ylabel("Time (seconds)")
plt.legend()

# Save the plot as a PNG file
plt.savefig(f"windows_program_log_filtered{entries}_colorcoded.png")

# Show the plot (optional)
plt.show()

# Display statistics
print("Statistics for the most recent 100 time entries:")
print(f"Average: {average_time:.2f} seconds")
print(
    f"Dynamic Threshold ({threshold_multiplier} Std Dev): {dynamic_threshold:.2f} seconds"
)
