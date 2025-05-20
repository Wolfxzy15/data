import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("Students Social Media Addiction.csv")

# Set page config
st.set_page_config(page_title="📱 Social Media Addiction Analysis", layout="centered")

# Title
st.title("📱 Student Social Media Addiction Dashboard")
st.markdown("Explore trends and patterns in student behavior related to social media use.")

# Show raw data
with st.expander("📄 Click to view the raw dataset"):
    st.dataframe(df)

# Basic info
st.subheader("🔍 Dataset Overview")
col1, col2 = st.columns(2)
with col1:
    st.write("**Rows:**", df.shape[0])
    st.write("**Columns:**", df.shape[1])
with col2:
    st.write("**Missing values per column:**")
    st.dataframe(df.isnull().sum())

# Select column to visualize
st.subheader("📊 Visualize Column Distribution")
column = st.selectbox("Select a column to view value counts", df.columns)

if df[column].dtype == 'object' or len(df[column].unique()) < 20:
    st.bar_chart(df[column].value_counts())
else:
    fig, ax = plt.subplots()
    ax.hist(df[column].dropna(), bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f'Histogram of {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    st.pyplot(fig)


# Correlation Heatmap (for numeric columns)
st.subheader("📈 Correlation Between Numeric Factors")
numeric_df = df.select_dtypes(include='number')

if numeric_df.shape[1] >= 2:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
else:
    st.info("Not enough numeric columns to display a correlation heatmap.")

# Filter and explore
st.subheader("🔍 Filter by Gender or Age Group")
if 'Gender' in df.columns:
    selected_gender = st.selectbox("Select Gender", ['All'] + df['Gender'].dropna().unique().tolist())
    if selected_gender != 'All':
        df = df[df['Gender'] == selected_gender]

if 'Age' in df.columns:
    age_range = st.slider("Select Age Range", int(df['Age'].min()), int(df['Age'].max()), (15, 25))
    df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

st.write("Filtered Data Preview", df.head())

# Download filtered data
st.download_button("💾 Download Filtered Data", df.to_csv(index=False), "filtered_students.csv", "text/csv")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
