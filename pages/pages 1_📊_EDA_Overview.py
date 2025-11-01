import streamlit as st
import pandas as pd
import os
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="EDA Overview", page_icon="📊", layout="wide")

# --- Đường dẫn ---
BASE_PATH = r"C:\Users\ADMIN\Downloads\HKN"
DATA_PATH = os.path.join(BASE_PATH, "data", "df_clean_mapped.csv")
PLOT_PATH = os.path.join(BASE_PATH, "assets", "plots")
BG_PATH = os.path.join(BASE_PATH, "assets", "bg_food.jpg")

# ---------------- BACKGROUND (không overlay, không filter) ----------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

background_base64 = get_base64_image(BG_PATH)

page_bg = f"""
<style>
/* === Ảnh nền chỉ hiển thị, KHÔNG có lớp phủ hoặc filter === */
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* === Nội dung chính === */
.block-container {{
    color: #ffffff;
    z-index: 2;
}}

/* === Sidebar === */
[data-testid="stSidebar"] {{
    background-color: rgba(255,255,255,0.9);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(200,200,200,0.3);
}}

/* === Font chữ === */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif;
}}

/* === Tiêu đề & chữ === */
h1, h2, h3, h4 {{
    color: #ffffff !important;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    font-weight: 700 !important;
}}

p, span, li {{
    color: #f5f5f5 !important;
    text-shadow: 1px 1px 5px rgba(0,0,0,0.7);
}}

[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
    color: #ffffff !important;
    text-shadow: 1px 1px 6px rgba(0,0,0,0.8);
    font-weight: 700 !important;
}}

[data-testid="stDataFrame"] table {{
    background-color: rgba(255,255,255,0.97);
    color: #000;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(255,255,255,0.15);
}}

.footer {{
    text-align: center;
    color: #dddddd;
    font-size: 14px;
    margin-top: 50px;
    text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

df = pd.read_csv(DATA_PATH, nrows=50000)

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center; font-size:46px;'>📊 Exploratory Data Analysis – Food Recommendation System</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:#eeeeee; font-size:18px;'>Tổng quan dữ liệu và biểu đồ trực quan (EDA).</p>",
    unsafe_allow_html=True,
)

# ---------------- DATASET OVERVIEW ----------------
st.header("1️⃣ Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Số dòng", f"{df.shape[0]:,}")
col2.metric("Số cột", df.shape[1])
col3.metric("User_id", df["user_id"].nunique())

st.dataframe(df.head(10), use_container_width=True)

st.subheader("📉 Thông tin dữ liệu")
st.write(df.describe().T)

# ---------------- VISUALIZATIONS ----------------
st.header("2️⃣ Biểu đồ trực quan")

st.subheader("⭐ Phân bố điểm đánh giá (Rating Distribution)")
st.image(os.path.join(PLOT_PATH, "rating_distribution.png"), use_column_width=True)

st.subheader("🍲 Top 10 món ăn phổ biến nhất")
st.image(os.path.join(PLOT_PATH, "top_recipes.png"), use_column_width=True)

st.subheader("🥦 Top 10 nguyên liệu thường gặp nhất")
st.image(os.path.join(PLOT_PATH, "top_ingredients.png"), use_column_width=True)

st.subheader("📅 Xu hướng điểm đánh giá theo tháng")
st.image(os.path.join(PLOT_PATH, "monthly_rating_trend.png"), use_column_width=True)

st.subheader("🍎 Mối tương quan giữa dinh dưỡng và đánh giá")
st.image(os.path.join(PLOT_PATH, "correlation_heatmap.png"), use_column_width=True)

st.subheader("💬 Word Cloud – Review của người dùng")
st.image(os.path.join(PLOT_PATH, "wordcloud_reviews.png"), use_column_width=True)

# ---------------- FOOTER ----------------
st.markdown("<hr style='border:1px solid rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
st.markdown(
    "<p class='footer'>© 2025 Group 10 | Food Recommendation System | Data Source: Food.com Dataset</p>",
    unsafe_allow_html=True,
)
