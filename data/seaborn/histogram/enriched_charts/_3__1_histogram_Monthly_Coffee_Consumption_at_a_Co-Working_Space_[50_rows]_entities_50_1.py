
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Data
data = {
    "Expense": [
        1200, 1350, 1400, 1450, 1500, 1550, 1600, 1625, 1700, 1750, 1800, 1850, 1900,
        1950, 2000, 2050, 2100, 2200, 2250, 2300, 2350, 2400, 2450, 2500, 2550, 2600,
        2650, 2700, 2750, 2800, 2850, 2900, 2950, 3000, 3100, 3200, 3250, 3300, 3350,
        3400, 3450, 3500, 3600, 3700, 3800, 3900, 4000, 4100, 4200, 4300, 4400, 4500,
        4600, 4700, 4800, 4900, 5000, 5100, 5200, 5300, 5400, 5500, 5600, 5700, 5800,
        5900, 6000
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Set the size of the plot
plt.figure(figsize=(14, 10))

# Create a histogram with specified bin width, color, and other properties
sns.histplot(df['Expense'], bins=15, color='#2ca02c', kde=False, binwidth=500, orientation='horizontal')

# Set title and labels for the plot
plt.title("Distribution of Monthly Household Expenses")
plt.xlabel("Frequency")
plt.ylabel("Expense (USD)")

# Show the plot
plt.show()