import random

import matplotlib.pyplot as plt

# Define constants
GUARD_TIME = 2200  # Guard time in milliseconds (typical value)
PREAMBLE = 128  # Preamble transmission time (typical value)

# Simulation parameters
MAX_DRIFT = 50  # Maximum tolerated clock drift (adjustable)
NUM_SIM_STEPS = 1000  # Number of simulation steps

# Function to calculate maximum resynchronization period
def max_resync_period(drift):
    return GUARD_TIME - 2 * PREAMBLE / 2*abs(drift)

# Simulate clock drift and resynchronization
drift_rates = []
resync_periods = []
for i in range(NUM_SIM_STEPS):
    # Generate random drift value within the specified range
    drift = (random.random() - 0.5) * MAX_DRIFT

    # Calculate maximum resynchronization period based on drift
    resync_period = max_resync_period(drift)

    # Update lists for plotting
    drift_rates.append(drift)
    resync_periods.append(resync_period)

# Generate plot
plt.figure(figsize=(8, 6))
plt.plot(drift_rates, resync_periods, label="Max Resync Period (ms)")
plt.xlabel("Clock Drift (ppm)")
plt.ylabel("Max Resync Period (ms)")
plt.title("Max Resync Period vs. Clock Drift (IEEE 802.15.4)")
plt.grid(True)
plt.legend()

# Save plot to folder (adjust folder path as needed)
plt.savefig("resync_period_vs_drift.png", dpi=300, bbox_inches="tight")

# Analyze drifting rate (example)
average_drift = sum(drift_rates) / len(drift_rates)
print(f"Average Clock Drift: {average_drift:.2f} ppm")

plt.show()