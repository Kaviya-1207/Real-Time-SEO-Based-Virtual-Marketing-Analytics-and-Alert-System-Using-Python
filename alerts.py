import pandas as pd

data = pd.read_csv("data/seo_data.csv")
data["Traffic_Change_%"] = data["Traffic"].pct_change() * 100

threshold = -10

print("Alert System Output:")
for index, row in data.iterrows():
    if row["Traffic_Change_%"] <= threshold:
        print(f"ALERT: Traffic dropped by {row['Traffic_Change_%']:.2f}% on {row['Date']}")
