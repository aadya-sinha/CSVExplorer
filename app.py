import streamlit as st
import pandas as pd 
import plotly.express as px

#Page configuration & File Upload
st.set_page_config(page_title="CSV Explorer", layout="wide")

st.title("CSV Explorer")
st.write("Upload a CSV or Excel file to explore its contents and visualize the data.")


uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlxs"])


if uploaded_file is None:
    st.info("Upload a file to get started.")
    st.stop()


#Loading the data
@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

df = load_data(uploaded_file)

st.success(f"File loaded - {df.shape[0]} rows, {df.shape[1]} columns")


#Data Preview
st.subheader("Data Preview")

col1, col2 = st.columns([3,1])
with col1:
    st.dataframe(df.head(50), use_container_width=True)
with col2:
    st.markdown("### Summary")
    st.write(f"**Rows:** {df.shape[0]}")
    st.write(f"**Columns:** {df.shape[1]}")
    st.write(f"**Missing values:** {df.isnull().sum().sum()}")
    st.markdown("### Column Types")
    st.dataframe(df.dtypes.astype(str).rename("Type"))



#Column Statistics
st.subheader("Column Statistics")
numeric_cols = df.select_dtypes(include="number").columns.tolist()

if numeric_cols:
    st.dataframe(df[numeric_cols].describe().T, use_container_width=True)
else:
    st.warning("No numeric columns found in the dataset.")


#Interactive Visualization
st.subheader("Chart Builder")

all_cols = df.columns.tolist()

col1, col2, col3 = st.columns(3)
with col1:
    chart_type = st.selectbox("Chart type", ["Bar", "Line", "Scatter", "Histogram"])
with col2:
    x_col = st.selectbox("X axis", all_cols)
with col3:
    y_col = st.selectbox("Y axis", numeric_cols if numeric_cols else all_cols )


if st.button("Generate Chart"):
    fig = None
    if chart_type == "Bar":
        fig = px.bar(df, x=x_col, y=y_col)
    elif chart_type == "Line":
        fig = px.line(df, x=x_col, y=y_col)
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_col, y=y_col)
    elif chart_type == "Histogram":
        fig = px.histogram(df, x=x_col)
    elif chart_type == "Box":
        fig = px.box(df, x=x_col, y=y_col)

    if fig:
        st.plotly_chart(fig, use_container_width=True)



#Filtering and Download
st.subheader("Filter Data")


filter_col = st.selectbox("Filter by column", all_cols)
unique_vals = df[filter_col].dropna().unique().tolist()
selected_vals = st.multiselect(f"Select values from '{filter_col}'", unique_vals, default=unique_vals[:5])

filtered_df = df[df[filter_col].isin(selected_vals)]
st.write(f"Showing {len(filtered_df)} rows")
st.dataframe(filtered_df, use_container_width=True)

csv_download = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Data", csv_download, "filtered_data.csv", "text/csv")



