import pandas as pd

airports_df = pd.read_csv("airports_df.csv", index_col=0)

print(airports_df["Time.Month"].head())

# airports_df.rename(columns={"Season": "Time.Season"}, inplace=True)

# airports_df.drop(
#     columns=[
#         "Unnamed: 0.4",
#         "Unnamed: 0.3",
#         "Unnamed: 0.2",
#         "Unnamed: 0.1",
#         "Unnamed: 0",
#         "Unnamed",
#     ],
#     inplace=True,
#     errors="ignore",
# )

# airports_df.to_csv("airports_df.csv")
print(airports_df.columns)


months_list = airports_df["Time.Month"].unique()
print(type(months_list))
