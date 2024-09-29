
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = {
    'Average_Monthly_Rainfall': [
        78.5, 102.3, 115.7, 94.6, 123.4, 88.1, 67.8, 101.2, 110.5,
        95.3, 84.7, 105.9, 93.2, 77.4, 99.8, 111.7, 88.4, 107.6,
        92.3, 102.1, 87.9, 113.5, 109.4, 97.1, 78.8, 90.2, 105.3,
        99.1, 85.6, 112.4, 102.7, 115.2, 91.4, 103.9, 98.7, 77.3,
        84.9, 109.7, 112.1, 101.4, 100.2, 96.8, 88.3, 110.8, 111.3,
        107.2, 103.1, 98.9, 94.1, 90.7
    ]
}

df = pd.DataFrame(data)

plt.figure(figsize=(10, 8))

sns.histplot(df['Average_Monthly_Rainfall'], color="#e74c3c", binwidth=3, kde=True)

plt.title('Distribution of Average Monthly Rainfall', pad=20)
plt.xlabel('Rainfall (mm)')
plt.ylabel('Frequency')

plt.show()