import streamlit as st
import pandas as pd
import pickle
import os
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Food Recommendation", page_icon="🍴", layout="wide")

# ------------------ PATHS ------------------
BASE_PATH = r"C:\Users\ADMIN\Downloads\HKN\data\data"
RECOMMEND_FILE = os.path.join(BASE_PATH, "recommendations.pkl")
RECIPE_INFO_FILE = os.path.join(BASE_PATH, "recipe_info.pkl")

# ------------------ LOAD MODELS ------------------
@st.cache_data
def load_pickles():
    try:
        with open(RECOMMEND_FILE, "rb") as f1:
            recommend_df = pickle.load(f1)
        with open(RECIPE_INFO_FILE, "rb") as f2:
            recipe_info = pickle.load(f2)
        return recommend_df, recipe_info
    except Exception as e:
        st.error(f"Lỗi khi load model hoặc dữ liệu: {e}")
        return None, None

recommend_df, recipe_info = load_pickles()

# ------------------ HEADER ------------------
st.title("🍽️ Personalized Recipe Recommender")
st.markdown("#### Dự đoán và gợi ý món ăn dựa trên mô hình đã huấn luyện sẵn")

# ------------------ USER INPUT ------------------
st.sidebar.header("⚙️ Tuỳ chọn")
user_id = st.sidebar.text_input("Nhập User ID:", "A3JWB4YXKHH5YY")
goal = st.sidebar.selectbox(
    "🎯 Mục tiêu ăn uống:",
    ["Giữ dáng", "Tăng cơ", "Tăng cân", "Ăn healthy", "Giảm cân"]
)
top_k = st.sidebar.slider("Số lượng món gợi ý:", 5, 20, 10)

# ------------------ DISPLAY MODEL STATUS ------------------
if recommend_df is not None:
    st.success("✅ Dữ liệu mô hình đã tải thành công!")
else:
    st.error("❌ Chưa thể tải dữ liệu mô hình, vui lòng kiểm tra lại file pkl.")

# ------------------ MAIN RECOMMENDATION LOGIC ------------------
if st.button("🔍 Xem gợi ý món ăn"):
    if recommend_df is not None and recipe_info is not None:
        # Giả sử recommend_df có cột ['user_id', 'recipe_id', 'est']
        user_recs = recommend_df[recommend_df["user_id"] == user_id]
        if user_recs.empty:
            st.warning("Không tìm thấy user này trong mô hình.")
        else:
            top_recipes = user_recs.sort_values(by="est", ascending=False).head(top_k)
            merged = top_recipes.merge(recipe_info, on="recipe_id", how="left")

            st.markdown(f"### 🧾 Top {top_k} món ăn được gợi ý cho **{user_id}** – ({goal})")

            # Hiển thị bảng kết quả
            st.dataframe(
                merged[["recipe_id", "name", "est", "minutes", "calories", "fat", "protein", "rating"]]
                .rename(columns={
                    "recipe_id": "ID món ăn",
                    "name": "Tên món",
                    "est": "Điểm dự đoán",
                    "minutes": "Thời gian (phút)",
                    "calories": "Calo",
                    "fat": "Chất béo",
                    "protein": "Đạm",
                    "rating": "Đánh giá TB"
                })
                .style.format({"Điểm dự đoán": "{:.3f}"})
            )

            # Biểu đồ trực quan nhỏ
            st.bar_chart(merged.set_index("name")["est"])
    else:

        st.error("Không thể chạy mô hình – vui lòng kiểm tra file pkl.")
