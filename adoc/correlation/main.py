import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Create a DataFrame

# Read the data from a CSV file
df = pd.read_csv("gateway.csv", header=None)

# Calculate the difference between the third and second columns
df['difference'] =  abs(df[2] - df[1])

# Set the 'difference' column to 1 if the difference is greater than 0, otherwise 0
df['difference'] = np.where(df['difference'] > 0, 1, 0)
# Print the DataFrame with the added difference column


# Calculate the cumulative sum of the 'difference' column
df['cumulative_sum'] = df['difference'].cumsum()
print(df)
#save the genrated data
df['cumulative_sum'].to_csv('x_data.txt', index=False)

# Plot the difference
plt.plot(df['cumulative_sum'])  # Skip the first difference (NaN)
plt.xlabel('Index')
plt.ylabel('Difference')
plt.title('Difference Between Consecutive Values')
plt.show()




# num_samples = 100
# x_data = np.random.rand(num_samples)
# y_data = np.random.rand(num_samples)
#
# # Save the data to text files
# np.savetxt("x_data.txt", x_data)
# np.savetxt("y_data.txt", y_data)


# Assuming the data is in two text files, 'x_data.txt' and 'y_data.txt'
x1_data = np.loadtxt('Productionspread.txt')
y1_data = np.loadtxt('Productionspreadsim.txt')


x2_data = np.loadtxt('Standardspecific.txt')
y2_data = np.loadtxt('Standardspecificsim.txt')

x3_data = np.loadtxt('Temperaturedifferencies.txt')
y3_data = np.loadtxt('Temperaturedifferenciessim.txt')

# Create a DataFrame
df = pd.DataFrame({'OMNeT_Production_Spread_DATASET': x1_data,
                   'PRISM_Production_Spread_DATASET': y1_data,
                   'OMNeT_Standard_Specific_DATASET': x2_data,
                   'PRISM_Standard_Specific_DATASET': y2_data,
                   'OMNeT_Temperature_Differencies_DATASET': x3_data,
                   'PRISM_Temperature_Differencies_DATASET': y3_data
                   }
                  )

# Calculate correlation matrix
correlation_matrix = df.corr()
print(correlation_matrix)


#generate an image of corelation
fig = px.imshow(correlation_matrix, text_auto=True)
# Save the figure to a folder
fig.write_image('cumulative_sum.png', width=800, height=600)  # Replace 'your_folder' with the actual folder path

fig.show()

