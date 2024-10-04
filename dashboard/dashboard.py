import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Membaca Data
day_df = pd.read_csv("https://raw.githubusercontent.com/denisadwi793/bike-sharing/refs/heads/main/data/day.csv")
day_df.head()
hour_df = pd.read_csv("https://raw.githubusercontent.com/denisadwi793/bike-sharing/refs/heads/main/data/hour.csv")
hour_df.head()

#Set tittle untuk dashboard
st.title("Dashboard Bike Sharing Dataset")

#Assesing data
day_df.info()
day_df.describe()
day_df.isnull().sum()
day_df[day_df['cnt'] < 0]  
day_df[(day_df['temp'] < 0) | (day_df['temp'] > 1)]
day_df[~day_df['season'].isin([1, 2, 3, 4])]
print("Jumlah duplikasi: ", day_df.duplicated().sum())
Q1 = day_df['cnt'].quantile(0.25)
Q3 = day_df['cnt'].quantile(0.75)
IQR = Q3 - Q1
outlier_condition = (day_df['cnt'] < (Q1 - 1.5 * IQR)) | (day_df['cnt'] > (Q3 + 1.5 * IQR))
outliers = day_df[outlier_condition]
print("Outliers:\n", outliers)

hour_df.info()
hour_df.describe()
hour_df.isnull().sum()
hour_df[hour_df['cnt'] < 0]  
hour_df[(hour_df['temp'] < 0) | (hour_df['temp'] > 1)]
hour_df[~hour_df['season'].isin([1, 2, 3, 4])]
print("Jumlah duplikasi: ", hour_df.duplicated().sum())
#mengidentifikasi outlier hour
Q1_hour = hour_df['cnt'].quantile(0.25)
Q3_hour = hour_df['cnt'].quantile(0.75)
IQR_hour= Q3 - Q1
outlier_condition = (hour_df['cnt'] < (Q1 - 1.5 * IQR)) | (hour_df['cnt'] > (Q3 + 1.5 * IQR))
outliers = hour_df[outlier_condition]
print("Outliers:\n", outliers)

#mengidentifikasi outlier day
Q1_day = day_df['cnt'].quantile(0.25)
Q3_day = day_df['cnt'].quantile(0.75)
IQR_day = Q3_day - Q1_day
outlier_condition = (day_df['cnt'] < (Q1 - 1.5 * IQR)) | (day_df['cnt'] > (Q3 + 1.5 * IQR))
outliers =day_df[outlier_condition]
print("Outliers:\n", outliers)

# Menghapus atau mengidentifikasi outliers
Q1 = hour_df['cnt'].quantile(0.25)
Q3 = hour_df['cnt'].quantile(0.75)
outliers_hour = hour_df[(hour_df['cnt'] < (Q1_hour - 1.5 * IQR_hour)) | (hour_df['cnt'] > (Q3_hour + 1.5 * IQR_hour))]
outliers_day = day_df[(day_df['cnt'] < (Q1_day - 1.5 * IQR_day)) | (day_df['cnt'] > (Q3_day + 1.5 * IQR_day))]
print(outliers_hour)
print(outliers_day)

#Eksplorasi data hour_df
hour_df.describe(include="all")
day_df.describe(include="all")

#cleaning data
#Mengatasi outliers pada dataset hour_df dengan metode drop
Q1 = hour_df['cnt'].quantile(0.25)
Q3 = hour_df['cnt'].quantile(0.75)
IQR = Q3 - Q1

maximum = Q3 + (1.5 * IQR)
minimum = Q1 - (1.5 * IQR)

kondisi_lower_than = hour_df['cnt'] < minimum
kondisi_more_than = hour_df['cnt'] > maximum

hour_df_dropped = hour_df.drop(hour_df[kondisi_lower_than].index)
hour_df_dropped = hour_df_dropped.drop(hour_df_dropped[kondisi_more_than].index)
print("Dataset setelah drop outliers:\n", hour_df_dropped)
jumlah_baris_sebelum = len(hour_df)
print(f"Jumlah baris sebelum menghapus outliers: {jumlah_baris_sebelum}")
#mengganti tipe data dteday dengan datetime
day_df.head()
column = "dteday"
day_df[column] = pd.to_datetime(day_df[column])
day_df.info()

column = "dteday"
hour_df[column] = pd.to_datetime(hour_df[column])
hour_df.info()

hour_df_dropped.to_csv('hour_df_cleaned.csv') 
#EDA
#1. Bagaimana pengaruh waktu terhadap pola penyewaan sepeda?

hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['day_of_week'] = hour_df['dteday'].dt.day_name()
hour_df['hour'] = hour_df['hr']
peak_hours = hour_df.groupby(['day_of_week', 'hour'])['cnt'].sum().reset_index()
peak_hours['max_cnt'] = peak_hours.groupby('day_of_week')['cnt'].transform('max')
peak_peak_hours = peak_hours[peak_hours['cnt'] == peak_hours['max_cnt']]
print("Jam puncak penyewaan sepeda setiap hari:\n", peak_peak_hours)

#2.Bagaimana pengaruh dari faktor cuaca terhadap jumlah total pengguna sepeda pada hari kerja dibandingkan dengan hari libur atau tidak bekerja?
weather_workday_df = day_df[day_df["workingday"] == 1].groupby(["weathersit"]).cnt.sum().sort_values(ascending=False).reset_index()
# karena tidak ada cuaca 4 maka akan kita tambahkan cuaca 4 dengan cnt bernilai 0.
if not (weather_workday_df['weathersit'] == 4).any():
    new_row = pd.DataFrame({"weathersit": [4], "cnt": [0]})
    weather_workday_df = pd.concat([weather_workday_df, new_row], ignore_index=True)

weather_workday_df.rename(columns={
    "weathersit": "weather_index",
    "cnt": "users_count"
}, inplace=True)

weather_workday_df.head()

# Mengelompokkan berdasarkan 'weathersit' dan menjumlahkan 'cnt'
weather_workday_df = day_df[day_df["workingday"] == 1].groupby("weathersit")['cnt'].sum().sort_values(ascending=False).reset_index()

# Karena tidak ada cuaca 4 maka akan kita tambahkan cuaca 4 dengan cnt bernilai 0
if not (weather_workday_df['weathersit'] == 4).any():
    new_row = pd.DataFrame({"weathersit": [4], "cnt": [0]})
    weather_workday_df = pd.concat([weather_workday_df, new_row], ignore_index=True)

# Mengganti nama kolom
weather_workday_df.rename(columns={
    "weathersit": "weather_index",
    "cnt": "users_count"
}, inplace=True)
weather_workday_df.head()

#Visualisasi
#1Bagaimana pengaruh waktu terhadap pola penyewaan sepeda?
plt.figure(figsize=(12, 6))
sns.barplot(data=peak_peak_hours, x='hour', y='cnt', hue='day_of_week', palette='viridis')
plt.title('Jam Puncak Penyewaan Sepeda Setiap Hari')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(rotation=45)
plt.legend(title='Hari dalam Seminggu')
plt.tight_layout()
plt.ion()
# Jika tidak ada peringatan terkait groupby
plt.figure(figsize=(12, 6))
sns.barplot(data=peak_peak_hours, x='hour', y='cnt', hue='day_of_week', palette='viridis')
plt.title('Jam Puncak Penyewaan Sepeda Setiap Hari')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(rotation=45)
plt.legend(title='Hari dalam Seminggu')
plt.tight_layout()
plt.ion()

#2.Bagaimana pengaruh dari faktor cuaca terhadap jumlah total pengguna sepeda pada hari kerja dibandingkan dengan hari libur atau tidak bekerja?
fig, ax = plt.subplots()
labels_detail = [
    'Clear or Partly cloudy', 
    'Mist and/or Cloudy', 
    'Light Rain and/or Thunderstorm or Light Snow', 
    'Heavy Rain or Snow and Fog'
]
size = weather_workday_df["users_count"]
pie = plt.pie(size, startangle=0)
title = plt.title("Jumlah Total Pengguna di Tiap Cuaca\nPada Hari Bekerja (2011-2012)", fontsize=20)
title.set_ha("center")
plt.legend(
    pie[0], 
    labels_detail, 
    bbox_to_anchor=(0.65,-0.05), 
    loc="lower right", 
    bbox_transform=plt.gcf().transFigure
)
plt.ion() 

fig, ax = plt.subplots()
labels_detail = [
    'Clear or Partly cloudy', 
    'Mist and/or Cloudy', 
    'Light Rain and/or Thunderstorm or Light Snow', 
    'Heavy Rain or Snow and Fog'
]
size = weather_workday_df["users_count"]
pie = plt.pie(size, startangle=0)
title = plt.title("Jumlah Total Pengguna di Tiap Cuaca\nPada Hari Libur (2011-2012)", fontsize=20)
title.set_ha("center")
plt.legend(
    pie[0], 
    labels_detail, 
    bbox_to_anchor=(0.65,-0.05), 
    loc="lower right", 
    bbox_transform=plt.gcf().transFigure
)
plt.ion()




