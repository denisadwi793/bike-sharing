import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set the title of the app
st.title("Bike Sharing Data Analysis")

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/denisadwi793/bike-sharing/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/denisadwi793/bike-sharing/refs/heads/main/data/hour.csv")

# Display the first few rows of day_df
st.subheader("Day Dataframe")
st.write(day_df.head())

# Display summary statistics for day_df
st.subheader("Summary Statistics for Day Dataframe")
st.write(day_df.describe())

# Display the first few rows of hour_df
st.subheader("Hour Dataframe")
st.write(hour_df.head())

# Display summary statistics for hour_df
st.subheader("Summary Statistics for Hour Dataframe")
st.write(hour_df.describe())

# Check for missing values
st.subheader("Missing Values")
st.write("Day Dataframe Missing Values:", day_df.isnull().sum())
st.write("Hour Dataframe Missing Values:", hour_df.isnull().sum())

# Check for duplicates
st.subheader("Duplicate Values")
st.write("Day Dataframe Duplicates:", day_df.duplicated().sum())
st.write("Hour Dataframe Duplicates:", hour_df.duplicated().sum())

# Outlier detection
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    outlier_condition = (df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))
    return df[outlier_condition]

outliers_hour = detect_outliers(hour_df, 'cnt')
outliers_day = detect_outliers(day_df, 'cnt')

st.subheader("Outliers in Hour Dataframe")
st.write(outliers_hour)

st.subheader("Outliers in Day Dataframe")
st.write(outliers_day)

# Data Cleaning
hour_df_cleaned = hour_df.copy()
hour_df_cleaned = hour_df_cleaned[~hour_df_cleaned.index.isin(outliers_hour.index)]

st.subheader("Cleaned Hour Dataframe")
st.write(hour_df_cleaned.head())

# Convert dteday to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Exploratory Data Analysis
st.subheader("Exploratory Data Analysis")

# Group by weather situation and working day
day_grouped = day_df.groupby(["weathersit", "workingday"]).agg({"cnt": ["sum", "mean"]}).reset_index()
st.write(day_grouped)

# Visualizations
st.subheader("Total Users by Weather Condition on Working Days")
weather_workday_df = day_df[day_df["workingday"] == 1].groupby(["weathersit"]).cnt.sum().reset_index()
if not (weather_workday_df['weathersit'] == 4).any():
    new_row = pd.DataFrame({"weathersit": [4], "cnt": [0]})
    weather_workday_df = pd.concat([weather_workday_df, new_row], ignore_index=True)

fig1, ax1 = plt.subplots()
ax1.pie(weather_workday_df['cnt'], labels=['Clear', 'Mist', 'Light Rain', 'Heavy Rain'], autopct='%1.1f%%')
ax1.set_title("Total Users on Working Days by Weather Condition")
st.pyplot(fig1)

st.subheader("Total Users by Weather Condition on Non-Working Days")
weather_non_workday_df = day_df[day_df["workingday"] == 0].groupby(["weathersit"]).cnt.sum().reset_index()
if not (weather_non_workday_df['weathersit'] == 4).any():
    new_row = pd.DataFrame({"weathersit": [4], "cnt": [0]})
    weather_non_workday_df = pd.concat([weather_non_workday_df, new_row], ignore_index=True)

fig2, ax2 = plt.subplots()
ax2.pie(weather_non_workday_df['cnt'], labels=['Clear', 'Mist', 'Light Rain', 'Heavy Rain'], autopct='%1.1f%%')
ax2.set_title("Total Users on Non-Working Days by Weather Condition")
st.pyplot(fig2)

# Hourly analysis
hour_df['hr_group'] = hour_df['hr'].apply(lambda x: "Dawn" if x < 6 else ("Morning" if x < 11 else ("Afternoon" if x < 15 else ("Evening" if x < 18 else "Night"))))

grouped_hour = hour_df.groupby('hr_group')['cnt'].sum().sort_values()
fig3, ax3 = plt.subplots()
grouped_hour.plot(kind='bar', ax=ax3, color='skyblue')
ax3.set_title('Total Users by Hour Group')
ax3.set_xlabel('Hour Group')
ax3.set_ylabel('Total Users')
st.pyplot(fig3)

# Conclusion
st.subheader("Conclusion")
st.write("""
- The analysis shows a correlation between weather conditions and bike-sharing users.
- The number of users tends to decrease during adverse weather conditions.
- There is a peak in usage during the evening hours.
""")