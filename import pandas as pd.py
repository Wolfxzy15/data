import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("data job posts.csv")  # Ensure this is in the same folder as the script

st.set_page_config(page_title="Job Market Dashboard", layout="wide")
st.title("📊 Job Market Dashboard")

# Show dataset preview
st.markdown("### 🔍 Preview of the Dataset")
st.dataframe(df.head(10))

# Dataset summary
st.markdown("### 📌 Dataset Summary")
col1, col2 = st.columns(2)
with col1:
    st.write("**Rows:**", df.shape[0])
    st.write("**Columns:**", df.shape[1])
    st.write("**Missing Values:**")
    st.dataframe(df.isnull().sum())
with col2:
    st.dataframe(df.describe(include='all'))

st.markdown("---")

# Filters
st.markdown("## 🧭 Filter by Job Title and Location")
titles = df['Title'].dropna().unique()
locations = df['Location'].dropna().unique()

selected_titles = st.multiselect("Select Job Titles", sorted(titles), default=titles[:3])
selected_locations = st.multiselect("Select Locations", sorted(locations), default=locations[:3])

filtered_df = df[
    df['Title'].isin(selected_titles) & 
    df['Location'].isin(selected_locations)
]

st.markdown(f"### 🎯 Filtered Results ({len(filtered_df)} jobs)")
st.dataframe(filtered_df)

st.download_button("💾 Download Filtered Data", filtered_df.to_csv(index=False), "filtered_jobs.csv", "text/csv")

st.markdown("---")

# Visualizations
st.markdown("## 📈 Visual Insights")

st.subheader("🏢 Top 10 Hiring Companies")
st.bar_chart(df['Company'].value_counts().head(10))

st.subheader("💼 Top 10 Job Titles")
st.bar_chart(df['Title'].value_counts().head(10))

st.subheader("🌍 Top 10 Locations")
st.bar_chart(df['Location'].value_counts().head(10))

# Optional Heatmap
st.subheader("🧭 Heatmap of Job Titles vs Locations")
pivot = df.pivot_table(index='Title', columns='Location', aggfunc='size', fill_value=0)
pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).head(10).index]  # Top 10 titles

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot, cmap="Blues", annot=True, fmt="d", linewidths=0.5)
plt.xticks(rotation=45, ha='right')
plt.title("Job Distribution Heatmap")
st.pyplot(fig)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
