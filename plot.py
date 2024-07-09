import streamlit as st
import pandas as pd
import altair as alt

# Sample DataFrame

st.title("PLOT POC")
df = st.file_uploader("Upload .csv file", type={'csv'})
df = pd.read_csv(df, encoding= "windows-1252")
df = pd.DataFrame(df)
datatypes = pd.DataFrame({
    "Column name":df.columns,
    "Datatypes":df.dtypes.values
})
columns= df.columns.to_list()
print("columns:",columns)
print(df.columns)
# Sidebar for selecting chart type, x-axis, and y-axis
st.sidebar.header("Chart Settings")
chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart","Column Chart" "Line Chart", "Scatter Plot"])
x_axis = st.sidebar.selectbox("Select X-axis", df.columns)
y_axis = st.sidebar.selectbox("Select Y-axis", df.columns)
aggregation = ["SUM", "COUNT", "MAX", "MIN"]
# Available data types
data_types = ["int64", "float64", "object", "bool", "datetime64[ns]"]

# Function to generate the chart
def generate_chart(chart_type, x_axis, y_axis):
    st.write(x_axis)
    print("df:", df[x_axis].dtypes)
    # print("data_x:", data_x)
    st.write(y_axis)
    st.write(datatypes)

    # Create tabs for each column
    tabs = st.tabs(columns)
    # tabs = st.tabs(df.columns)

    # Dictionary to store new data types
    new_dtypes = {}

# Inject CSS for wrapping tabs
    st.markdown(
        """
        <style>
        .stTabs [role="tablist"] {
            flex-wrap: wrap;
        }
        .stTabs [role="tab"] {
            flex: 1 0 auto;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Iterate over each column and create a tab
    for i, col in enumerate(df.columns):
        with tabs[i]:
            st.write(f"Column: {col}")
            current_dtype = str(df[col].dtype)
            st.write(f"Current Data Type: {current_dtype}")

            # Select new data type
            new_dtype = st.selectbox(f"Select new data type for {col}", data_types, index=data_types.index(current_dtype))
            new_dtypes[col] = new_dtype

    # Button to apply changes
    if st.button("Apply Changes"):
        for col, dtype in new_dtypes.items():
            try:
                df[col] = df[col].astype(dtype)
                st.success(f"Changed {col} to {dtype}")
            except Exception as e:
                st.error(f"Could not change {col} to {dtype}: {e}")

    if df[x_axis].dtypes == "int64" or "float64":
        st.write (f"As {x_axis} column is of {df[x_axis].dtypes} datatype, please select the aggregation type")
    else:
        pass
        x_agg = st.sidebar.selectbox("Select the aggregation type for X-axis:", aggregation, placeholder="Select the aggregation funtion")
    if df[y_axis].dtypes == "int64" or "float64":
            st.write (f"As {y_axis} column is of {df[y_axis].dtypes} datatype, please select the aggregation type")
            y_agg = st.sidebar.selectbox("Select the aggregation type for Y-axis:", aggregation, placeholder="Select the aggregation funtion")
    
    if chart_type == "Bar Chart" && x_agg == "":
        chart = alt.Chart(df).mark_bar().encode(
            x=x_axis,
            y=y_axis
        )
    if chart_type == "Column Chart":
        chart = alt.Chart(df).mark_bar().encode(
            y=x_axis,
            x=y_axis
        )
    elif chart_type == "Line Chart":
        chart = alt.Chart(df).mark_line().encode(
            x=x_axis,
            y=y_axis
        )
    elif chart_type == "Scatter Plot":
        chart = alt.Chart(df).mark_point().encode(
            x=x_axis,
            y=y_axis
        )

    return chart

# Generate the chart based on user input
chart = generate_chart(chart_type, x_axis, y_axis)
st.altair_chart(chart, use_container_width=True)

# Display the DataFrame
st.write("### Data")
st.write(df)
