
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Data
data = {
    'Month': ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December'],
    'Average_Temperature': [5, 6, 10, 14, 18, 22, 26, 24, 20, 14, 9, 5]
}

# Create DataFrame
df = pd.DataFrame(data)

# Set the order of the months
df['Month'] = pd.Categorical(df['Month'], categories=[
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August', 'September',
    'October', 'November', 'December'], ordered=True)

# Plot the data
plt.figure(figsize=(12, 6))
ax = sns.lineplot(x='Month', y='Average_Temperature', data=df, 
                  marker='o', color='#FF5733')

# Annotations and labels
for x, y in zip(df['Month'], df['Average_Temperature']):
    ax.text(x, y, f'{y}°C', color='blue', ha='right', va='bottom')

# Customize appearance
ax.set_title('Monthly Average Temperature Change')
ax.set_xlabel('Month')
ax.set_ylabel('Temperature (°C)')
sns.set_style('whitegrid')

plt.show()