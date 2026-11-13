import pandas as pd

df = pd.read_csv("creditcard.csv")
print("Total rows:", len(df))
print("Columns:", list(df.columns))
print("Fraud distribution:\n", df['Class'].value_counts())
print("Fraud %:", (df['Class'].sum() / len(df)) * 100)
