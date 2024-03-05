import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def visualisasi_data_pertanyaan1(semua_data_df):
    peminjaman_pada_hari_kerja = semua_data_df[semua_data_df['workingday_day'] == 'Ya']['cnt_hour'].sum()
    peminjaman_pada_hari_libur = semua_data_df[semua_data_df['workingday_day'] == 'Tidak']['cnt_hour'].sum()

    data = {
        'Hari': ['Hari Kerja', 'Hari Libur'],
        'Jumlah Peminjaman': [peminjaman_pada_hari_kerja, peminjaman_pada_hari_libur]
    }
    df = pd.DataFrame(data)
    return df

def visualisasi_data_pertanyaan2(semua_data_df):
    df = semua_data_df[['hum_hour', 'cnt_hour']]
    return df

semua_data_df = pd.read_csv("dashboard/semua_data_df.csv")

data_pertanyaan1 = visualisasi_data_pertanyaan1(semua_data_df)
peminjaman_pada_hari_kerja = data_pertanyaan1.loc[data_pertanyaan1['Hari'] == 'Hari Kerja', 'Jumlah Peminjaman'].values[0]
peminjaman_pada_hari_libur = data_pertanyaan1.loc[data_pertanyaan1['Hari'] == 'Hari Libur', 'Jumlah Peminjaman'].values[0]

data_pertanyaan2 = visualisasi_data_pertanyaan2(semua_data_df)

st.sidebar.title('Dashboard Analisis Data Peminjaman Sepeda')
st.sidebar.write('Pada dashboard ini akan berisi 2 informasi yang bisa diakses dengan memilih salah satu pilihan dibawah ini.')

with st.sidebar.expander('Analisis Data - 1'):
    st.write('Perbandingan Jumlah Peminjaman Sepeda pada Hari Kerja dan Hari Libur.')
    
with st.sidebar.expander('Analisis Data - 2'):
    st.write('Korelasi Antara Tingkat Kelembapan dan Jumlah Peminjaman Sepeda.')

menu = st.sidebar.radio('Pilih Analisis:', ('Analisis Data - 1', 'Analisis Data - 2'))

if menu == 'Analisis Data - 1':
    st.header('Perbandingan Jumlah Peminjaman Sepeda pada Hari Kerja dan Hari Libur')
    with st.expander('Lihat Statistik Jumlah Peminjaman Sepeda'):
        st.write('Statistik Jumlah Peminjaman Sepeda')
        st.write('Jumlah Peminjaman Sepeda pada Hari Kerja:', peminjaman_pada_hari_kerja)
        st.write('Jumlah Peminjaman Sepeda pada Hari Libur:', peminjaman_pada_hari_libur)
    
    st.write('Visualisasi Perbandingan Jumlah Peminjaman Sepeda pada Hari Kerja dan Hari Libur')
    plt.figure(figsize=(5, 5))
    bars = plt.bar(['Hari Kerja', 'Hari Libur'], [peminjaman_pada_hari_kerja, peminjaman_pada_hari_libur], color=['grey', 'black'])
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom')
    
    plt.yscale('log')
    plt.title('Perbandingan Jumlah Peminjaman Sepeda pada Hari Kerja dan Hari Libur')
    plt.ylabel('Jumlah Peminjaman Sepeda')
    st.pyplot(plt)
    
    with st.expander('Kesimpulan'):
        st.write('Berdasarkan analisis yang sudah dilakukan, maka didapatkan jumlah peminjaman sepeda pada hari kerja lebih tinggi daripada peminjaman sepeda pada hari libur. Hal ini bisa diakibatkan karena beberapa kemungkinan seperti pada hari kerja, orang-orang lebih sering melakukan peminjaman sepeda untuk keperluan transportasi.')

elif menu == 'Analisis Data - 2':
    st.header('Korelasi Antara Tingkat Kelembapan dan Jumlah Peminjaman Sepeda')
    
    with st.expander('Nilai Korelasi'):
        korelasi = data_pertanyaan2['hum_hour'].corr(data_pertanyaan2['cnt_hour'])
        st.write(f"Korelasi antara tingkat kelembapan dan jumlah peminjaman sepeda: {korelasi}")
    
    st.write('Visualisasi Hubungan Antara Tingkat Kelembapan dan Jumlah Peminjaman Sepeda')
    plt.figure(figsize=(5, 5))
    sns.regplot(x='hum_hour', y='cnt_hour', data=data_pertanyaan2, scatter_kws={'alpha':0.3}, line_kws={'color': 'red'})
    plt.title('Hubungan antara Kelembapan dan Jumlah Peminjaman Sepeda')
    plt.xlabel('Tingkat Kelembapan')
    plt.ylabel('Jumlah Peminjaman Sepeda')
    st.pyplot(plt)
    
    with st.expander('Kesimpulan'):
        st.write('Berdasarkan analisis yang sudah dilakukan, maka didapatkan adanya hubungan negatif antara tingkat kelembapan dengan jumlah peminjaman sepeda sebesar -0,32. Dari data tersebut dapat didapatkan sebuah pola ketika tingkat kelembapan semakin tinggi, maka jumlah peminjaman sepeda akan cenderung lebih rendah. Ketika tingkat kelembapan semakin rendah, maka jumlah peminjaman sepeda akan cenderung lebih tinggi. Lebih jelasnya perihal pola dapat dilihat pada hasil visualisasi data yang sudah dilakukan, dimana garis tren yang ada menunjukkan hasil yang berbanding terbalik.')
