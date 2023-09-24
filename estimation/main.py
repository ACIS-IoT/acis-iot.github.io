import re

import numpy as np
from scipy.stats import expon
from scipy.optimize import minimize
import matplotlib.pyplot as plt

from datetime import datetime


import pandas as pd



import sys

# Check if the required number of parameters is provided
if len(sys.argv) < 3:
    print("Usage: python main.py [attack] [csv file] [time column] [attack column]")
    sys.exit(1)

# Access the command-line parameters
param1 = sys.argv[1]
param2 = sys.argv[2]
param3 = sys.argv[3]
param4 = sys.argv[4]

# Print the parameter values
print("attack: [", param1, "] csv file: [", param2, "] time column: [", param3, "] attack column: [", param4,"]")










# Define the input CSV file path
#input_file = 'data.csv'
input_file = param2
# Define the output CSV file path
output_file = 'output.csv'

# Define the specific string and date format to filter rows

specific_date_format = '%d/%m/%Y %I:%M:%S %p'

# Define the list of specific strings to filter rows
#specific_strings = ['DoS']
specific_strings = [param1]
# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file, sep=';', header=None)

# Create a boolean mask to filter rows based on specific strings
mask = df.apply(
    lambda row: any(
        any(specific_string in str(cell) for specific_string in specific_strings) for cell in row
    ),
    axis=1
)

# Apply the mask to the DataFrame to filter rows
filtered_df = df[mask]

# Specify the column numbers to filter
#column_numbers = [6, 84]  # Replace with the actual column numbers you want to filter

column_numbers = [int(param3), int(param4)]  # Replace with the actual column numbers you want to filter
# Filter the specified columns
filtered_columns = filtered_df.iloc[:, column_numbers]

# Set the header names for the filtered columns
header_names = ['TimeStamps', 'Attack']  # Replace with the desired header names

filtered_columns.columns = header_names

# Save the filtered DataFrame to a new CSV file
filtered_columns.to_csv(output_file, index=False)

##########################################################


# Read the dataset into a pandas DataFrame
df = pd.read_csv(output_file)

# Convert the date/time column to datetime data type
df['TimeStamps'] = pd.to_datetime(df['TimeStamps'], format='%d/%m/%Y %I:%M:%S %p')  # Replace 'DateTime' with the actual column name

# Sort the DataFrame by the date/time column
df = df.sort_values('TimeStamps')

# Calculate the time differences between consecutive attacks
time_diff = df['TimeStamps'].diff().dt.total_seconds()

# Remove the first row (NaN) from the time differences
time_diff = time_diff.dropna()

# Compute the mean time difference between attacks
mean_time_diff = time_diff.mean()

# Compute the attack rate based on exponential distribution
attack_rate = 1 / mean_time_diff#.total_seconds()

# Print the mean time between attacks and the attack rate
print("Mean time between attacks:", mean_time_diff, " seconds")
print("Estimated rate parameter using classical method:", attack_rate)


# Define the negative log-likelihood function for the exponential distribution
def neg_log_likelihood(params):
    rate = params[0]
    return -np.sum(expon.logpdf(mean_time_diff, scale=1 / rate))


# Initial guess for the rate parameter (lambda)
initial_guess = [1]

# Define the constraint to prevent rate parameter from becoming zero
bound = [(1e-8, None)]

# Use MLE to estimate the parameter by minimizing the negative log-likelihood
result = minimize(neg_log_likelihood, initial_guess, method='L-BFGS-B', bounds=bound)


# Get the estimated rate parameter
estimated_rate = result.x[0]

# Print the estimated rate parameter
print("Estimated rate parameter using MLE with solver L-BFGS-B:", estimated_rate)


# Use MLE to estimate the parameter by minimizing the negative log-likelihood
result = minimize(neg_log_likelihood, initial_guess, method='Nelder-Mead', bounds=bound)


# Get the estimated rate parameter
estimated_rate = result.x[0]

# Print the estimated rate parameter
print("Estimated rate parameter using MLE with Nelder-Mead:", estimated_rate)

#
# ###########################################################
# ###########################################################
# ###########################################################
# # Sorted dataset with attack timestamps
# dataset = [
#     ("2022-01-01 10:00:00", "attack1"),
#     ("2022-01-01 10:05:00", "attack2"),
#     ("2022-01-01 10:09:00", "attack2"),
#     ("2022-01-01 10:15:00", "attack3"),
#     ("2022-01-01 10:20:00", "attack3")
# ]
#
# # Initialize a list to store the time intervals between unique attacks
# time_intervals = []
#
# # Identify unique attacks
# unique_attacks = set([attack[1] for attack in dataset])
#
# # Iterate through the sorted dataset considering unique attacks
# for i in range(1, len(dataset)):
#     prev_attack = dataset[i - 1][1]
#     curr_attack = dataset[i][1]
#
#     # Consider only unique attacks
#     if curr_attack != prev_attack:
#         prev_timestamp = datetime.strptime(dataset[i - 1][0], "%Y-%m-%d %H:%M:%S")
#         curr_timestamp = datetime.strptime(dataset[i][0], "%Y-%m-%d %H:%M:%S")
#
#         # Calculate the time interval between unique attacks
#         time_interval =  (curr_timestamp - prev_timestamp).total_seconds()
#
#         # Store the time interval in the list
#         time_intervals.append(time_interval)
#
# # Print the time intervals between unique attacks
# for interval in time_intervals:
#     print(interval)
#
# # Sample interarrival times (time between attacks)
# interarrival_times =time_intervals
#
#
# # Define the negative log-likelihood function for the exponential distribution
# def neg_log_likelihood(params):
#     rate = params[0]
#     return -np.sum(expon.logpdf(interarrival_times, scale=1 / rate))
#
#
# # Initial guess for the rate parameter (lambda)
# initial_guess = [1]
#
# # Define the constraint to prevent rate parameter from becoming zero
# bound = [(1e-8, None)]
#
# # Use MLE to estimate the parameter by minimizing the negative log-likelihood
# result = minimize(neg_log_likelihood, initial_guess, method='L-BFGS-B', bounds=bound)
#
# # Extract the estimated rate parameter
# estimated_rate = result.x[0]
#
# print(f"Estimated rate parameter (lambda): {estimated_rate}")
#


# Plot the distribution
# plt.hist(time_intervals, bins=10, alpha=0.5, density=True, label='Original Data')
# plt.plot(np.sort(interarrival_times), np.exp(-estimated_rate * np.sort(interarrival_times)), 'r-', label='Exponential Distribution')
# plt.xlabel('Time Intervals')
# plt.ylabel('Probability Density')
# plt.legend()
# plt.show()
