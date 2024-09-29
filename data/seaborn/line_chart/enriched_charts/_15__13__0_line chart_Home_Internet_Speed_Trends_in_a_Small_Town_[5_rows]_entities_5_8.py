
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Data points from the given table
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
    'Average Reading Scores': [65, 67, 69, 66, 70, 72, 75, 77, 74, 78, 80, 82]
}

# Convert data into DataFrame
df = pd.DataFrame(data)

# Create the line plot
plt.figure(figsize=(12, 6))  # Modify width and height
sns.lineplot(x='Year', y='Average Reading Scores', data=df, color='#1f77b4')  # Change the color scheme

# Adding annotations for the start and end points
plt.text(2010, 65, 'Start', horizontalalignment='left', size='small', color='black')
plt.text(2021, 82, 'Latest', horizontalalignment='right', size='small', color='black')

# Setting the title and labels
plt.title('Annual Average Reading Scores from 2010 to 2021', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Average Reading Scores', fontsize=12)

sns.despine()
plt.show()