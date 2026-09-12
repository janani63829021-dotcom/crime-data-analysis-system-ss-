import streamlit as st
import pandas as pd


st.title("🕵️ Crime Data Analysis System")


# Upload Crime Data
st.sidebar.header("📂 Upload Crime Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, skipinitialspace=True)
else:
    df = pd.read_csv("crime_data.csv", skipinitialspace=True)

df.columns = df.columns.str.strip()

# Convert Date
df["Date"] = pd.to_datetime(
    df["Date"].astype(str).str.strip(),
    dayfirst=True,
    errors="coerce"
)

# Crime Data
st.subheader("📋 Crime Data")
st.dataframe(df)

# Summary Cards
st.subheader("📊 Crime Analysis")

col1, col2, col3 = st.columns(3)

col1.metric("Total Crimes", len(df))
col2.metric("Crime Types", df["Crime_Type"].nunique())
col3.metric("Locations", df["Location"].nunique())

# Filters
st.subheader("🔎 Filter Crime Data")

crime_types = df["Crime_Type"].dropna().unique()

selected_crime = st.selectbox(
    "Select Crime Type",
    ["All"] + list(crime_types)
)

locations = df["Location"].dropna().unique()

selected_location = st.selectbox(
    "Select Location",
    ["All"] + list(locations)
)

# Reset Button
if st.button("🔄 Reset Filters"):
    st.rerun()

# Create filtered data
filtered_df = df.copy()

# Crime Type Filter
if selected_crime != "All":
    filtered_df = filtered_df[
        filtered_df["Crime_Type"] == selected_crime
    ]

# Location Filter
if selected_location != "All":
    filtered_df = filtered_df[
        filtered_df["Location"] == selected_location
    ]

# Date Filter
st.subheader("📅 Filter by Date")

use_date = st.checkbox("Filter by Date")

if use_date:
    selected_date = st.date_input("Select Date")

    filtered_df = filtered_df[
        filtered_df["Date"].dt.date == selected_date
    ]

# Search
st.subheader("🔍 Search Crime Data")

search_text = st.text_input(
    "Search crime, location or description"
)

if search_text:
    filtered_df = filtered_df[
        filtered_df.astype(str).apply(
            lambda row: row.str.contains(
                search_text,
                case=False,
                na=False
            ).any(),
            axis=1
        )
    ]

# Filtered Data
st.subheader("📋 Filtered Crime Data")
st.dataframe(filtered_df)

st.metric("Filtered Crimes", len(filtered_df))

# Filtered Crime Analysis
st.subheader("📊 Filtered Crime Analysis")

filtered_crime_count = filtered_df["Crime_Type"].value_counts()

st.bar_chart(filtered_crime_count)

# Crime Type Analysis
st.subheader("📊 Crime Type Analysis")

crime_count = df["Crime_Type"].value_counts()

st.bar_chart(crime_count)

# Location-wise Analysis
st.subheader("📍 Location-wise Crime Analysis")

location_count = df["Location"].value_counts()

st.bar_chart(location_count)

# Date-wise Analysis
st.subheader("📅 Date-wise Crime Analysis")

date_count = df.groupby("Date").size()

st.line_chart(date_count)

# Most Common Crime
st.subheader("🚨 Most Common Crime")

most_common_crime = df["Crime_Type"].value_counts().idxmax()
most_common_count = df["Crime_Type"].value_counts().max()

st.write("Most Common Crime:", most_common_crime)
st.write("Number of Cases:", most_common_count)

# Download Report
st.subheader("📥 Download Crime Report")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="crime_report.csv",
    mime="text/csv"
)

# Crime Hotspot
st.subheader("📍 Crime Hotspot")

top_location = df["Location"].value_counts().idxmax()
top_location_count = df["Location"].value_counts().max()

st.write("Highest Crime Location:", top_location)
st.write("Number of Cases:", top_location_count)

# Crime Percentage
st.subheader("📈 Crime Percentage")

crime_percentage = (
    df["Crime_Type"]
    .value_counts(normalize=True) * 100
).round(2)

st.bar_chart(crime_percentage)
# Crime Summary
st.subheader("📋 Crime Summary")

summary = df["Crime_Type"].value_counts().reset_index()

summary.columns = [
    "Crime Type",
    "Number of Cases"
]

st.dataframe(summary)
