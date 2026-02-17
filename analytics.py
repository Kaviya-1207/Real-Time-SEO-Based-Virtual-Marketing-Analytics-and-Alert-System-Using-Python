import pandas as pd

data = pd.read_csv("data/seo_data.csv")

data["Traffic_Change_%"] = data["Traffic"].pct_change() * 100

print("SEO Analytics Data:")
print(data)
