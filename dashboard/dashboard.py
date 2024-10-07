import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set the title of the app
st.title("Bike Sharing Data Analysis")

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/denisadwi793/bike-sharing/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/denisadwi793/bike-sharing/refs/heads/main/data/hour.csv")


# Visualizations
weather_workday_df = day_df[day_df["workingday"] == 1].groupby(["weathersit"]).cnt.sum().reset_index()
if not (weather_workday_df['weathersit'] == 4).any():
    new_row = pd.DataFrame({"weathersit": [4], "cnt": [0]})
    weather_workday_df = pd.concat([weather_workday_df, new_row], ignore_index=True)

fig1, ax1 = plt.subplots()
ax1.pie(weather_workday_df['cnt'], labels=['Clear', 'Mist', 'Light Rain', 'Heavy Rain'], autopct='%1.1f%%')
ax1.set_title("Jumlah Total Pengguna di Tiap Cuaca Pada Hari Bekerja (2011-2012")
st.pyplot(fig1)


weather_non_workday_df = day_df[day_df["workingday"] == 0].groupby(["weathersit"]).cnt.sum().reset_index()
if not (weather_non_workday_df['weathersit'] == 4).any():
    new_row = pd.DataFrame({"weathersit": [4], "cnt": [0]})
    weather_non_workday_df = pd.concat([weather_non_workday_df, new_row], ignore_index=True)

fig2, ax2 = plt.subplots()
ax2.pie(weather_non_workday_df['cnt'], labels=['Clear', 'Mist', 'Light Rain', 'Heavy Rain'], autopct='%1.1f%%')
ax2.set_title("Jumlah Total Pengguna di Tiap Cuaca Pada Hari Libur (2011-2012")
st.pyplot(fig2)

# Hourly analysis
hour_df['hr_group'] = hour_df['hr'].apply(lambda x: "Dawn" if x < 6 else ("Morning" if x < 11 else ("Afternoon" if x < 15 else ("Evening" if x < 18 else "Night"))))

grouped_hour = hour_df.groupby('hr_group')['cnt'].sum().sort_values()
fig3, ax3 = plt.subplots()
grouped_hour.plot(kind='bar', ax=ax3, color='skyblue')
ax3.set_title('Jumlah total kelompok pengguna tiap kelompok jam ')
ax3.set_xlabel('Kelompok Jam')
ax3.set_ylabel('Total Pengguna')
st.pyplot(fig3)

# Conclusion
st.subheader(Kesimpulan")
st.write("""
- Jadi dapat disimpulkan bahwa terdapat korelasi diantara faktor cuaca dan total pengguna Bike Sharing baik pada hari kerja maupun hari libur atau tidak bekerja, dikarenakan keduanya saling bersesuaian dan tidak berlawanan. Pie Chart diatas merupakan salah satu faktor pendukung bahwa Faktor Cuaca yang menyebabkan adanya hubungan yang bersesuaian antara Faktor Cuaca di hari bekerja dan Faktor Cuaca di hari libur dengan Total pengguna Bike Sharing. Salah satu faktor pendukung lainnya berada di Eksplorasi Data day_df dimana meskipun total pengguna Bike Sharing di setiap cuaca pada hari bekerja lebih besar dibandingkan dengan total pengguna di setiap cuaca pada hari libur tetapi rata-rata diantara kedua hari tersebut tidak berbeda jauh pada masing-masing cuaca sehingga dapat disimpulkan bahwa semakin cuaca menjadi buruk atau ekstrim maka semakin sedikit total pengguna baik di hari bekerja maupun di hari libur.
- Jadi dapat disimpulkan bahwa terdapat korelasi di tiap kelompok jam yang dikelompokkan berdasarkan Waktu dan total pengguna, salah satu faktor pendukung bahwa terdapat korelasi atau hubungan antara jumlah pengguna sepeda pada jam-jam tertentu adalah Bar Char di atas, di mana pada pengguna lebih banyak aktif menggunakan Bike Sharing di malam hari.
""")