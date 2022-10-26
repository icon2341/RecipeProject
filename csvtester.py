from datetime import datetime

import datetime
import pandas as pd

df = pd.read_csv("recipes.csv")

df = df.head(10000)
drop_cols = [x for x in df.columns if "Content" in x]
drop_cols = drop_cols + ["AuthorId", "RecipeId", "PrepTime", "TotalTime", "Calories", "RecipeYield", "Images",
                         "Keywords"]
df = df.drop(columns=drop_cols)

print(df.head())
print(df.describe())

print(df.columns)

for column in df.columns:
    print(f"{column}: ", df[column].isna().sum())

print(f"Unique Categories: {df['RecipeCategory'].unique()}")

# print(df["CookTime"])
print(df["CookTime"].isna().sum())

# df["CookTime"] = [x if parse('PT{}H', str(x)) else None for x in df["CookTime"]]


for index, value in enumerate(df["CookTime"]):
    value = str(value)
    try:
        time_value = datetime.datetime.strptime(value, "PT%HH%MM")
    except ValueError:
        try:
            time_value = datetime.datetime.strptime(value, "PT%HH")
        except ValueError:
            try:
                time_value = datetime.datetime.strptime(value, "PT%MM")
            except:
                continue

    df["CookTime"][index] = time_value

#for index, value in enumerate(df["CookTime"]):
#    if type(value) is str:
#        df["CookTime"][index] = None
df["CookTime"] = [None if type(x) is not datetime.datetime else x.strftime("%H:%M") for x in df["CookTime"]]
print([x for x in df["CookTime"].unique()])
df = df.dropna()
df.to_csv("AlteredRecipes.csv")
