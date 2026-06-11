import numpy as np
import pandas as pd

data = {
    "Name": ["Arjun", "Chethan", "Hamsa", "Ravi", "Anu"],
    "Math": [85, 70, 90, 60, 75],
    "Science": [80, 65, 95, 55, 70],
    "English": [78, 72, 88, 60, 68]
}

df = pd.DataFrame(data)

subjects = ["Math", "Science", "English"]

for col in subjects:
    mean = df[col].mean()
    std = df[col].std()
    df[col] = (df[col] - mean) / std

print("\nZ-Score Normalized Data:\n")
print(df)