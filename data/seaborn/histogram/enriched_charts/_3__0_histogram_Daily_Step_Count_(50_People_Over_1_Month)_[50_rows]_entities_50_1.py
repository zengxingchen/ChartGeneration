
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

data = {
    'Hours': [
        1, 3, 2, 4, 5, 6, 4, 7, 8, 5,
        3, 2, 1, 6, 5, 7, 8, 4, 3, 2,
        9, 10, 11, 8, 6, 7, 5, 4, 3, 2,
        1, 10, 12, 9, 8, 7, 6, 5, 4, 3,
        2, 11, 10, 9, 8, 7, 6, 5, 4, 3,
        2, 1, 0, 14, 15, 12, 13, 10, 11, 12,
        10, 9, 8, 7, 6, 5, 4, 3, 2, 1
    ]
}

df = pd.DataFrame(data)

plt.figure(figsize=(10, 8))

sns.histplot(data=df, y='Hours', color='#FF5733', binwidth=1.5, kde=True, orientation='vertical')

plt.title('Weekly Exercise Hours Distribution in a Sample Population')
plt.xlabel('Frequency')
plt.ylabel('Hours Spent on Exercise per Week')
plt.grid(True)

plt.show()