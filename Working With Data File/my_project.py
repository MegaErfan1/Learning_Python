import pandas as pd


file_path = "products.csv"
df = pd.read_csv(file_path)
df["Total Price"] = df["Quantity"] * df["Price"]
output_path = "processed_products.csv"
df.to_csv(output_path, index=False)
print("The file has been processed and saved as: ", output_path)
print(df.head())
