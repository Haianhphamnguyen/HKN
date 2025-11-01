import streamlit as st
import base64
import os

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Recipe Recommender System",
    page_icon="🍽️",
    layout="wide"
)

# ------------------ LOAD BACKGROUND IMAGE ------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"

background_image_path = os.path.join("assets", "bg_food.jpg")
background_base64 = get_base64_image(background_image_path)

# ------------------ CUSTOM CSS ------------------
page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    position: relative;
}}

[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(15, 15, 15, 0.93);
    z-index: -1;
}}

[data-testid="stSidebar"] {{
    background-color: rgba(255,255,255,0.9);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(200,200,200,0.3);
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif;
    color: #ffffff;
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(15px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.big-title {{
    text-align: center;
    font-size: 56px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 3px 3px 10px rgba(0,0,0,0.9);
    margin-top: 13vh;
    animation: fadeIn 1s ease-in-out;
}}

.sub-title {{
    text-align: center;
    font-size: 22px;
    color: #f1f1f1;
    font-weight: 500;
    margin-top: -5px;
    animation: fadeIn 1.5s ease-in-out;
}}

.description {{
    text-align: center;
    color: #f7f7f7;
    font-size: 18px;
    margin: 25px auto;
    max-width: 720px;
    line-height: 1.7;
    text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
    animation: fadeIn 2s ease-in-out;
}}

hr {{
    border: 1px solid rgba(255,255,255,0.25);
    width: 65%;
    margin: 25px auto;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🍴 Food Recommendation System")
st.sidebar.markdown("Chọn trang ở thanh bên để xem nội dung:")

# ------------------ MAIN CONTENT ------------------
st.markdown("<div class='big-title'>🍽️ Recipe Recommender System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>👩‍💻 Group 10 — Data Science Project</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ NAVIGATION / DESCRIPTION ------------------
st.markdown("""
<div class='description'>
Dự án khai thác dữ liệu từ Food.com để xây dựng hệ thống gợi ý công thức món ăn phù hợp từng người dùng.<br>
Khám phá các phần chính trong dự án:
</div>
""", unsafe_allow_html=True)

st.markdown("""
#### 📊 **1. Exploratory Data Analysis (EDA)**
- Tổng quan dữ liệu, thống kê tần suất đánh giá, xu hướng người dùng, các đặc trưng dinh dưỡng.
- Hiển thị biểu đồ tương tác, heatmap và wordcloud.

#### 🤖 **2. Recommendation System**
- Gợi ý món ăn dựa trên hành vi người dùng và đặc trưng món ăn.
- Cho phép chọn mô hình SVD hoặc Hybrid.
- Hiển thị hiệu suất model (RMSE, MAE) và Top 20 món được đề xuất.
""")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#ccc;'>👉 Mở tab <b>📊 EDA Overview</b> hoặc <b>🤖 Recommendation Model</b> ở sidebar để xem chi tiết.</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#aaa;'>© 2025 Group 10 — Data Science Project | UCSD</p>",
    unsafe_allow_html=True
)
