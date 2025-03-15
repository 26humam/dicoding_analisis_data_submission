import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# membuat page title
st.set_page_config(page_title="Dashboard Analisis Penyewaan Sepeda", layout="wide")

# mengload data df_day.csv
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "df_day.csv")
    # file_path = "df_day.csv"
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("File tidak ditemukan. Pastikan file tersedia di lokasi yang benar.")
        return pd.DataFrame()

df = load_data()

# membuat sidebar
with st.sidebar:
    # menambahkan logo
    st.image("logo.png")
    st.title("Rental Sepeda")

    st.sidebar.header("Filter Rentang Waktu")
    year_option = st.sidebar.radio("Pilih Tahun:", ['2011 & 2012', '2011', '2012'])

# mapping dan filter data
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df['season'] = df['season'].map(season_mapping)
df['season'] = pd.Categorical(df['season'], categories=["Spring", "Summer", "Fall", "Winter"], ordered=True)
df['month'] = pd.to_datetime(df['dteday']).dt.month
df['yr'] = df['yr'].map({0: 2011, 1: 2012})

if year_option != '2011 & 2012':
    df = df[df['yr'] == int(year_option)]

# membuat tampilan dashboard utama
st.header("📊 Dashboard Analisis Penyewaan Sepeda")
if year_option == '2011 & 2012':
    st.write("### Data Penyewaan Sepeda Tahun 2011 dan 2012")
else:
    st.write(f"### Data Penyewaan Sepeda Tahun {year_option}")


# membuat tampilan data total penyewaan sepeda per tahun
col1, col2, col3 = st.columns(3)

with col1:
    total_casual = df['casual'].sum()
    st.metric("Total Casual Rentals", value=total_casual)

with col2:
    total_registered = df['registered'].sum()
    st.metric("Total Registered Rentals", value=total_registered)

with col3:
    total_rentals = df['cnt'].sum()
    st.metric("Total Rentals", value=total_rentals)

# visualisasi 1: Penyewaan Sepeda per Musim
st.subheader("Perkembangan Penyewaan Sepeda per Musim")
seasonal_data = df.groupby(['season', 'yr'])['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='season', y='cnt', hue='yr', data=seasonal_data, palette={2011: 'blue', 2012: 'green'}, ax=ax)
plt.xlabel("Musim")
plt.ylabel("Total Penyewaan")
plt.title("Total Penyewaan Sepeda per Musim")
st.pyplot(fig)

# visualisasi 2: Tren Penyewaan Sepeda per Bulan
st.subheader("Tren Penyewaan Sepeda per Bulan")
monthly_data = df.groupby(['month', 'yr'])['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='month', y='cnt', hue='yr', data=monthly_data, marker='o', palette={2011: 'blue', 2012: 'green'}, ax=ax)
plt.xlabel("Bulan")
plt.ylabel("Total Penyewaan")
plt.title("Tren Penyewaan Sepeda per Bulan")
st.pyplot(fig)

# conclusion
st.subheader("📝 Kesimpulan Analisis")
st.markdown(
    "✅ **Musim Semi (Spring) menunjukkan lonjakan signifikan dibandingkan tahun sebelumnya**.\n"
    "\n✅ **Musim Gugur (Fall) memiliki jumlah penyewaan tertinggi**.\n"
    "\n✅ **Lonjakan besar terjadi di awal tahun, terutama Januari hingga Maret**.\n"
    "\n✅ **Terjadi penurunan tren di akhir tahun (Oktober - Desember)**.\n"
    "\n✅ **Total persentase kenaikan penyewaan sepeda dari 2011 ke 2012: 64.88%**."
)

st.subheader("📜 Data Penyewaan Sepeda")
st.dataframe(df)
