import pandas as pd

# read data from Excel file
file_path = 'Steam_paid_game_stats.xlsx'
xls = pd.ExcelFile(file_path)

# look at the sheet names
print("工作表名称:", xls.sheet_names)

# read data from the first sheet
df = pd.read_excel(xls, sheet_name='Sheet1')

# print the first few rows of the data
print("数据预览:")
print(df.head())

# look at the basic information of the data
print("\n数据基本信息:")
print(df.info())

# make sure the data has the required columns
required_columns = ['Sub-Genre', 'Revenue']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"数据中缺少必要列: {required_columns}")

# calculate the total revenue for each Sub-Genre
subgenre_revenue = df.groupby('Sub-Genre')['Revenue'].sum().reset_index()
subgenre_revenue.rename(columns={'Revenue': 'Total Revenue'}, inplace=True)

# merge the revenue data with the original data
df = df.merge(subgenre_revenue, on='Sub-Genre')

# calculate the revenue percentage for each game
df['Revenue Percentage'] = df['Revenue'] / df['Total Revenue']

# calculate the HHI contribution for each Sub-Genre
df['HHI Contribution'] = df['Revenue Percentage'] ** 2
hhi = df.groupby('Sub-Genre')['HHI Contribution'].sum().reset_index()

# calculate the HHI for each Sub-Genre
hhi['HHI'] = hhi['HHI Contribution'] * 10000

# print the HHI for each Sub-Genre
print("\n每个 Sub-Genre 的 HHI:")
print(hhi[['Sub-Genre', 'HHI']])

# save the HHI data to an Excel file
output_file_path = 'SubGenre_HHI.xlsx'
hhi[['Sub-Genre', 'HHI']].to_excel(output_file_path, index=False)

print(f"\nHHI 结果已保存到 {output_file_path}")