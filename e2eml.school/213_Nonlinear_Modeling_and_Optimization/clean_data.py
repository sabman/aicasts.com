import pandas as pd

df = pd.read_csv("AKC Breed Info.csv")
df.dropna()
print(df.head())
