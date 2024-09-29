
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

data = {
    'scores': [
        75, 85, 92, 88, 76, 95, 83, 77, 91, 80,
        97, 82, 89, 78, 84, 79, 94, 87, 81, 86,
        90, 98, 73, 74, 100, 99, 96, 93, 71, 72,
        69, 70, 68, 66, 64, 65, 67, 62, 61, 63,
        60, 58, 57, 56, 55, 54, 52, 53, 51, 50,
        48, 47, 46, 45, 44, 43, 42, 41, 40, 39,
        38, 37, 36, 35, 34, 33, 32, 31, 30, 29,
        28, 27, 26, 25, 24, 23, 22, 21, 20, 19,
        18, 17, 16, 15, 14, 13, 12, 11, 10, 9,
        8, 7, 6, 5, 4, 3, 2, 1
    ]
}

df = pd.DataFrame(data)

sns.set(style="whitegrid")
plt.figure(figsize=(10, 14))

sns.histplot(data=df, x='scores', color="#3498db", binwidth=5, kde=False, orientation='horizontal')

plt.title('Test Scores Distribution', pad=20)
plt.xlabel('Frequency')
plt.ylabel('Scores')

plt.show()