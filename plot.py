import matplotlib.pyplot as plt
import numpy as np

# Algorithms and their data
algorithms = [
    "ID", "ID+CN+LD", "ID+CN+LD+SD", "ID+CN+SD", "ID+CN+SD+LD",
    "ID+LD+CN", "ID+LD+CN+SD", "ID+LD+SD+CN", "ID+SD", "ID+SD+CN",
    "ID+SD+CN+LD", "ID+SD+LD+CN", "ID+SD+LDF", "LDF", "SD",
    "SD+CN+ID", "SD+CN+ID+LD", "SD+CN+LD", "SD+CN+LD+ID", "SD+ID",
    "SD+ID+CN", "SD+ID+CN+LD", "SD+ID+LD+CN", "SD+ID+LDF",
    "SD+LD+CN", "SD+LD+CN+ID", "SD+LD+ID+CN", "SL"
]

total_colors = [
    1932, 1878, 1853, 1833, 1853,
    1878, 1853, 1853, 1975, 1833,
    1855, 1855, 1975, 1975, 1730,
    1689, 1719, 1693, 1719, 1712,
    1694, 1725, 1725, 1715,
    1695, 1719, 1719, 1878
]

total_time = [
    110.50, 132.93, 129.59, 143.45, 129.17,
    139.25, 126.56, 119.08, 667.00, 139.51,
    131.47, 129.22, 660.94, 32.36, 116.22,
    140.50, 132.90, 127.98, 133.57, 440.30,
    130.36, 123.71, 123.23, 645.89,
    124.03, 132.88, 129.22, 259.70
]

avg_colors = [
    38.64, 37.56, 37.06, 36.66, 37.06,
    37.56, 37.06, 37.06, 39.50, 36.66,
    37.10, 37.10, 39.50, 39.50, 34.60,
    33.78, 34.38, 33.86, 34.38, 34.24,
    33.88, 34.50, 34.50, 34.30,
    33.90, 34.38, 34.38, 37.56
]

avg_time = [
    2.21, 2.66, 2.59, 2.87, 2.58,
    2.79, 2.53, 2.38, 13.34, 2.79,
    2.63, 2.58, 13.22, 0.65, 2.32,
    2.81, 2.66, 2.56, 2.67, 8.81,
    2.61, 2.47, 2.46, 12.92,
    2.48, 2.66, 2.58, 5.19
]

# Function to plot histogram with ascending order
def plot_sorted_histogram(values, title, ylabel):
    sorted_indices = np.argsort(values)
    sorted_values = np.array(values)[sorted_indices]
    sorted_algorithms = np.array(algorithms)[sorted_indices]

    x_pos = np.arange(len(sorted_algorithms))
    plt.figure(figsize=(18,6))
    plt.bar(x_pos, sorted_values, color='skyblue')
    plt.xticks(x_pos, sorted_algorithms, rotation=90)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()

# Plot 4 sorted histograms
plot_sorted_histogram(total_colors, "Total Colors Used by 28 Algorithms (Ascending)", "Total Colors")
plot_sorted_histogram(total_time, "Total Time by 28 Algorithms (Ascending)", "Time (s)")
plot_sorted_histogram(avg_colors, "Average Colors Used by 28 Algorithms (Ascending)", "Avg Colors")
plot_sorted_histogram(avg_time, "Average Time by 28 Algorithms (Ascending)", "Avg Time (s)")
