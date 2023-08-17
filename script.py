import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create a DataFrame from the provided data
data = {
    "LOCATION": ["DNK", "DNK", "DNK", "DNK", "DNK", "DNK", "DNK", "DNK", "DNK", "DNK"],
    "TIME": ["2015-Q1", "2015-Q2", "2015-Q3", "2015-Q4", "2016-Q1", "2016-Q2", "2016-Q3", "2016-Q4", "2017-Q1", "2017-Q2"],
    "Value": [99.16666, 100.1333, 100.8667, 99.86667, 100.9333, 101.5, 101.5, 101.5, 102.5667, 103.1]
}

df = pd.DataFrame(data)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
# Replace 'dataset.csv' with the actual path to your dataset


# Convert TIME column to datetime format
#df['TIME'] = pd.to_datetime(df['TIME'], format='%Y-Q%q')

# Basic statistics
print(df.describe())

# Visualize the CPI trend over time
plt.figure(figsize=(12, 6))
sns.lineplot(x='TIME', y='Value', data=df)
plt.title('CPI Trend for Housing Rentals in Denmark')
plt.xlabel('Time')
plt.ylabel('CPI Value')
plt.xticks(rotation=45)
plt.savefig('0.png') 
plt.close()

# Visualize CPI distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Value', bins=15, kde=True)
plt.title('Distribution of CPI Values for Housing Rentals')
plt.xlabel('CPI Value')
plt.ylabel('Frequency')
plt.savefig('1.png') 
plt.close()

# Correlation between CPI and time
plt.figure(figsize=(10, 6))
sns.scatterplot(x='TIME', y='Value', data=df)
plt.title('Correlation between CPI and Time')
plt.xlabel('Time')
plt.ylabel('CPI Value')
plt.xticks(rotation=45)
plt.savefig('2.png') 
plt.close()
