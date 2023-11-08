import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Define a threshold to ignore massive outliers
outlier_threshold = 100.0  # You can adjust this threshold as needed

# Read the time entries from the file and filter out outliers
with open("windows_program_log.txt", "r") as file:
    time_entries = [
        float(line.strip())
        for line in file.readlines()
        if float(line.strip()) <= outlier_threshold
    ]

# Calculate statistics
average_time = np.mean(time_entries)
median_time = np.median(time_entries)
std_deviation = np.std(time_entries)

# Create a plot
plt.figure(figsize=(10, 6))  # You can adjust the figure size as needed
plt.plot(time_entries, marker="o", linestyle="-")
plt.title("Windows Program Log (Outliers Ignored)")
plt.xlabel("Entry Number")
plt.ylabel("Time (seconds)")

# Save the plot as a PNG file
plt.savefig("windows_program_log_filtered.png")

# Show the plot (optional)
plt.show()

# Display statistics
print("Statistics for time entries:")
print(f"Average: {average_time:.2f} seconds")
print(f"Median: {median_time:.2f} seconds")
print(f"Standard Deviation: {std_deviation:.2f} seconds")
