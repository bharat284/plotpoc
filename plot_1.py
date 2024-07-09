import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.title("PLOT POC")

# Upload CSV file
uploaded_file = st.file_uploader("Upload .csv file", type='csv')

if uploaded_file is not None:
    # Read CSV file
    df = pd.read_csv(uploaded_file, encoding="windows-1252")
    
    # Display the DataFrame
    st.write("### Data")
    st.write(df)
    
    # Display the DataFrame with column names and data types
    datatypes = pd.DataFrame({
        "Column name": df.columns,
        "Datatypes": df.dtypes.values
    })
    # column_dt_group = group_columns_by_datatype(df)
    # Sidebar for selecting chart type, x-axis, and y-axis
    st.sidebar.header("Chart Settings")
    chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart", "Column Chart", "Line Chart", "Scatter Plot"])
    x_axis = st.sidebar.selectbox("Select X-axis", df.columns)
    y_axis = st.sidebar.selectbox("Select Y-axis", df.columns)
    aggregation = ["SUM","MEAN", "COUNT", "MAX", "MIN"]
    # Optional color selection
    color_column = st.sidebar.selectbox('Select column for color (optional):', ["None"] + list(df.columns))
    
    # Available data types
    data_types = ["int64", "float64", "object", "bool", "datetime64[ns]"]
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
    # Function to display lists horizontally
    def display_list_horizontally(title, column_list):
        if column_list:
            formatted_list = ", ".join(column_list)
        else:
            formatted_list = "None"
        st.subheader(title)
        st.write(formatted_list)
    column_groups = group_columns_by_datatype(df)
    # Create individual lists for each data type
    object_columns = list(column_groups.get(np.dtype('O'), []))
    int64_columns = list(column_groups.get(np.dtype('int64'), []))
    float64_columns = list(column_groups.get(np.dtype('float64'), []))
    datetime_columns = list(column_groups.get(np.dtype('<M8[ns]'), []))
    if object_columns is not None:
        display_list_horizontally("object_columns:",object_columns)
    else:
        pass
    if int64_columns is not None:
        display_list_horizontally("int64_columns:",int64_columns)
    else:
        pass
    if float64_columns is not None:
        display_list_horizontally("float64_columns:",float64_columns)
    else:
        pass
    if datetime_columns is not None:
        display_list_horizontally("datetime_columns:",datetime_columns)
    else:
        pass
    # Function to generate the chart
    def generate_chart(chart_type, x_axis, y_axis, color_column = None):
        st.write(datatypes)
        
        st.write ()
        
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

        # Create tabs for each column
        columns= df.columns.to_list()
        tabs = st.tabs(columns)

        # Dictionary to store new data types
        new_dtypes = {}

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

        # Display aggregation options if necessary
        if df[x_axis].dtypes in ["int64", "float64"]:
            x_agg = st.sidebar.selectbox(f"Select the aggregation type for {x_axis}:", aggregation, key="x_agg", placeholder="Select Aggregation function")
        else:
            x_agg = None
        
        if df[y_axis].dtypes in ["int64", "float64"]:
            y_agg = st.sidebar.selectbox(f"Select the aggregation type for {y_axis}:", aggregation, key="y_agg", placeholder="Select Aggregation function")
        else:
            y_agg = None

        # Aggregate the data if aggregation is selected
        if x_agg:
            df[x_axis] = df.groupby(x_axis)[y_axis].transform(x_agg.lower())
        if y_agg:
            df[y_axis] = df.groupby(x_axis)[y_axis].transform(y_agg.lower())

        # Generate chart based on user input
        try:
            if chart_type == "Bar Chart":
                chart = alt.Chart(df).mark_bar().encode(
                    x=x_axis,
                    y=y_axis, 
                    color=alt.Color(color_column, scale=alt.Scale(scheme='category20')) if color_column else alt.value('steelblue')
                )
            elif chart_type == "Column Chart":
                chart = alt.Chart(df).mark_bar().encode(
                    x=y_axis,
                    y=x_axis,
                    color=alt.Color(color_column, scale=alt.Scale(scheme='category20')) if color_column else alt.value('steelblue')
                )
            elif chart_type == "Line Chart":
                chart = alt.Chart(df).mark_line().encode(
                    x=x_axis,
                    y=y_axis,
                    color=alt.Color(color_column, scale=alt.Scale(scheme='category20')) if color_column else alt.value('steelblue')
                )
            elif chart_type == "Scatter Plot":
                chart = alt.Chart(df).mark_point().encode(
                    x=x_axis,
                    y=y_axis,
                    color=alt.Color(color_column, scale=alt.Scale(scheme='category20')) if color_column else alt.value('steelblue')
                )
            else:
                st.error("Unsupported chart type")
                return None
            return chart
        except Exception as e:
            st.error(f"Error generating chart: {e}")
            return None
    # Generate the chart based on user input
    if color_column != "None":
        chart = generate_chart(chart_type, x_axis, y_axis, color_column)
    else:
        chart = generate_chart(chart_type, x_axis, y_axis)
    st.altair_chart(chart, use_container_width=True)
