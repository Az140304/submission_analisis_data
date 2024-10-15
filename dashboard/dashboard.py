import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import streamlit as st

all_data = pd.read_csv("all_data.csv") 
order_payments = pd.read_csv("../data/olist_order_payments_dataset.csv")
orders = pd.read_csv("../data/olist_orders_dataset.csv")
customers = pd.read_csv("../data/olist_customers_dataset.csv")

st.sidebar.title("Menu Navigasi")
menu = st.sidebar.selectbox("Menu:", ["Home", "Pertanyaan Satu", "Pertanyaan Dua"])
if menu == "Home" or menu is None:
    st.title('Projek Analisis Data : E-Commerce Public Dataset ')
    st.write(f"**Nama**  : Azhar Fikri H.")
    st.write(f"**Email**  : afharyodwiseno@gmail.com")
    st.write(f"**ID DIcoding**  : afharyo")

    st.header("Library yang Digunakan")
    st.markdown("- numpy")
    st.markdown("- pandas")
    st.markdown("- matplotlib")
    st.markdown("- datetime")

    st.header("Dataset yang Digunakan")

    d1, d2, d3 = st.tabs(["orders", "order_payments", "customers"])

    with d1:
        st.write(orders.head(10))
        

    with d2:
        st.write(order_payments.head(10))

    with d3:
        st.write(customers.head(10))
        
    
    
    st.caption('Copyright (c) 2024')
elif menu == "Pertanyaan Satu":

    st.header("1. Kota manakah dengan total pembelian terbesar di platform Olist pada tahun 2018 ?")
    st.subheader("Hasil Visualisasi Data")
    all_data['order_approved_at'] = pd.to_datetime(all_data['order_approved_at'])

    df1 = all_data[all_data['order_approved_at'].dt.year == 2018]
    df1 = df1.groupby(['customer_state'])['payment_value'].agg('sum')
    df1 = df1.sort_values(ascending=True).head(10)

    x = []
    y = []

    for state, count in df1.items():
        x.append(state)
        y.append(count)



    plt.figure(figsize=(12, 10))


    plt.barh(x, y, height=0.7)
    plt.xlabel("Total Pemebelian")
    plt.ylabel("Kota")
    plt.title("Negara dengan Total Pembelian Terbesar pada Tahun 2018")
    plt.show()
    st.pyplot(plt.show())

    st.subheader("Kesimpulan")
    st.write("Pada tahun 2018, kota dengan total pembelian terbesar ada di kota Sao Paolo (SP). Kemudian, kota dengan total pembelian terkecil ada di kota Acre (AC) yang jumlahnya berdekatan dengan kota Roraima (RR)")

elif menu == "Pertanyaan Dua":
    st.header("2. Bagaimana tren aktivitas pembelian barang pada tahun 2017 dari bulan ke bulan?")
    st.subheader("Hasil Visualisasi Data")
    all_data['order_approved_at'] = pd.to_datetime(all_data['order_approved_at'])

    df2 = all_data[all_data['order_approved_at'].dt.year == 2017]
    df2_monthly = df2.resample('M', on='order_approved_at').size()

    # Plot the data as a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(df2_monthly.index, df2_monthly.values, marker='o', linestyle='-', color='b')
    plt.title("Tren Aktivitas Membeli Barang pada tahun 2017")
    plt.xlabel("Tanggal")
    plt.ylabel("Number of Orders")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.show())

    st.subheader("Kesimpulan")

    st.write("Dari bulan ke bulan, platform Olist menunjukkan tren peningkatan dalam halnya jumlah aktivitas pembelian barang pada tahun 2017. Menjelang tahun 2018, aktivitas pembelian sempat mencapai puncaknya.")
    st.caption('Copyright (c) 2024')