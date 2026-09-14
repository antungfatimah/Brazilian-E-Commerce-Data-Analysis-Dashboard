import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")

# ---------------------------------------------------------------
# Load data
# ---------------------------------------------------------------
# Pakai path relatif terhadap lokasi file ini, bukan cwd saat dijalankan.
# Ini penting karena Streamlit Cloud menjalankan app dari root repo,
# sedangkan kalau dijalankan lokal biasanya dari dalam folder dashboard/.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "main_data.csv")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    return df


main_df = load_data()

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📊 E-Commerce Public Dataset Dashboard")
st.markdown(
    "Dashboard ini menyajikan hasil analisis data e-commerce untuk menjawab "
    "dua pertanyaan bisnis utama: tren jumlah order bulanan dan performa "
    "revenue per kategori produk."
)

# ---------------------------------------------------------------
# Sidebar filter
# ---------------------------------------------------------------
st.sidebar.header("Filter")

delivered_df = main_df[main_df["order_status"] == "delivered"].copy()
delivered_df = delivered_df[
    (delivered_df["order_month"] >= "2017-01") & (delivered_df["order_month"] <= "2018-08")
]

min_month = delivered_df["order_month"].min()
max_month = delivered_df["order_month"].max()
month_options = sorted(delivered_df["order_month"].unique())

selected_months = st.sidebar.select_slider(
    "Rentang Bulan",
    options=month_options,
    value=(min_month, max_month),
)

filtered_df = delivered_df[
    (delivered_df["order_month"] >= selected_months[0])
    & (delivered_df["order_month"] <= selected_months[1])
]

# ---------------------------------------------------------------
# Metrics ringkas
# ---------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Order", f"{filtered_df['order_id'].nunique():,}")
col2.metric("Total Revenue", f"R$ {filtered_df['price'].sum():,.2f}")
col3.metric("Rata-rata Review Score", f"{filtered_df['review_score'].mean():.2f}")

st.divider()

# ---------------------------------------------------------------
# Pertanyaan Bisnis 1: Tren order bulanan
# ---------------------------------------------------------------
st.subheader("1. Tren Jumlah Order Bulanan")

monthly_orders = (
    filtered_df.drop_duplicates("order_id")
    .groupby("order_month")["order_id"]
    .nunique()
    .reset_index(name="order_count")
    .sort_values("order_month")
)

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(monthly_orders["order_month"], monthly_orders["order_count"], marker="o", color="#1f77b4")
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Jumlah Order")
plt.xticks(rotation=45)
st.pyplot(fig1)

# ---------------------------------------------------------------
# Pertanyaan Bisnis 2: Revenue & review per kategori
# ---------------------------------------------------------------
st.subheader("2. Top 10 Kategori Produk Berdasarkan Revenue")

category_summary = (
    filtered_df.groupby("product_category_name_english")
    .agg(
        total_revenue=("price", "sum"),
        total_items_sold=("order_item_id", "count"),
        avg_review_score=("review_score", "mean"),
    )
    .reset_index()
    .sort_values("total_revenue", ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=category_summary,
    y="product_category_name_english",
    x="total_revenue",
    color="#1f77b4",
    ax=ax2,
)
ax2.set_xlabel("Total Revenue")
ax2.set_ylabel("Kategori Produk")
st.pyplot(fig2)

with st.expander("Lihat tabel detail kategori"):
    st.dataframe(category_summary, use_container_width=True)

st.caption(
    "Data: E-Commerce Public Dataset (Olist). Dibuat untuk proyek analisis data — "
    "Dicoding 'Belajar Analisis Data dengan Python'."
)
