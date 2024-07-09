import streamlit as st
import pandas as pd

# Sample DataFrame (replace with your actual DataFrame)
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago'],
    'Salary': [50000, 60000, 70000],
    'Join Date': ['2020-01-01', '2018-05-15', '2015-11-20']
}
df = pd.DataFrame(data)

# Function to group columns by data type
def group_columns_by_datatype(df):
    groups = {}
    for col in df.columns:
        dtype = df[col].dtype
        if dtype not in groups:
            groups[dtype] = [col]
        else:
            groups[dtype].append(col)
    return groups

# Group columns by data type
column_groups = group_columns_by_datatype(df)
print(column_groups)

# # Display each group in Streamlit
# st.title('Columns Grouped by Data Type')

# for dtype, columns in column_groups.items():
#     st.subheader(f"{dtype} Columns")
#     st.write(columns)

