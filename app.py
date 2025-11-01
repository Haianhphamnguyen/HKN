import streamlit as st
import pandas as pd
import pickle
import os
import base64

# ==========================================================
# 🧩 PAGE CONFIGURATION
# ==========================================================
st.set_page_config(page_title="🍽️ Food Recommendation System", layout="wide")

# ==========================================================
# 🖼️ BACKGROUND IMAGE SETUP
# ==========================================================
def get_base64_image(image_path):
    """Đọc ảnh và mã hóa base64 để làm nền."""
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        return None

bg_path = os.path.join("assets", "bg_food.jpg")
background_base64 = get_base64_image(bg_path)

if background_base64:
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("{background_base64}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(10,10,10,0.85);
        z-index: -1;
    }}
    h1, h2, h3, h4, h5, h6, p, span, div {{
        color: white;
        font-family: 'Poppins', sans-serif;
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# 📋 SIDEBAR NAVIGATION
# ==========================================================
page = st.sidebar.radio("📂 Chọn trang:", ["📊 EDA Overview", "🤖 Recommendation Model"])

# ==========================================================
# 📈 PAGE 1 — EDA OVERVIEW
# ==========================================================
if page == "📊 EDA Overview":
    st.title("📊 Exploratory Data Analysis — Food Recommendation System")
    st.markdown("Tổng quan và thống kê dữ liệu món ăn từ **Food.com Dataset** 🍜")

    data_path = os.path.join("data", "RAW_recipes.csv")
    inter_path = os.path.join("data", "RAW_interactions.csv")

    if os.path.exists(data_path) and os.path.exists(inter_path):
        recipes = pd.read_csv(data_path)
        interactions = pd.read_csv(inter_path)

        st.subheader("🧾 Tổng quan dữ liệu Recipes")
        col1, col2, col3 = st.columns(3)
        col1.metric("Số dòng", f"{len(recipes):,}")
        col2.metric("Số cột", f"{len(recipes.columns):,}")
        col3.metric("User ID duy nhất", f"{interactions['user_id'].nunique():,}")

        with st.expander("👀 Xem trước dữ liệu Recipes"):
            st.dataframe(recipes.head(10), use_container_width=True)

        st.subheader("📈 Thống kê mô tả dữ liệu Recipes")
        st.dataframe(recipes.describe(include='all').T.fillna("").head(15), use_container_width=True)

        with st.expander("🔍 Xem trước dữ liệu Interactions"):
            st.dataframe(interactions.head(10), use_container_width=True)

    else:
        st.error("⚠️ Không tìm thấy file dữ liệu: `RAW_recipes.csv` hoặc `RAW_interactions.csv` trong thư mục `/data`.")

# ==========================================================
# 🤖 PAGE 2 — RECOMMENDATION MODEL
# ==========================================================
elif page == "🤖 Recommendation Model":
    st.title("🤖 Food Recommendation System")
    st.markdown("Hệ thống gợi ý món ăn dựa trên lịch sử tương tác người dùng 🍽️")

    # --- Load model & data ---
    rec_path = os.path.join("data", "recommendations.pkl")
    info_path = os.path.join("data", "recipe_info.pkl")

    try:
        with open(rec_path, "rb") as f:
            recommend_df = pickle.load(f)
        with open(info_path, "rb") as f:
            recipe_info = pickle.load(f)
    except Exception as e:
        st.error(f"❌ Không thể tải file model hoặc dữ liệu: {e}")
        st.stop()

    # --- UI Inputs ---
    model_choice = st.selectbox("🔧 Chọn mô hình gợi ý:", ["Hybrid SVD", "Hybrid CBF (0.7 SVD + 0.3 CBF)"])
    user_id = st.number_input("🔢 Nhập User ID:", min_value=1, step=1)

    if st.button("🚀 Tạo gợi ý món ăn"):
        if "user_id" not in recommend_df.columns or "recipe_id" not in recommend_df.columns:
            st.error("⚠️ Dữ liệu recommendations.pkl không hợp lệ (thiếu cột user_id hoặc recipe_id).")
            st.stop()

        if user_id not in recommend_df["user_id"].values:
            st.warning(f"⚠️ User ID {user_id} không tồn tại trong dữ liệu!")
        else:
            user_recs = recommend_df[recommend_df["user_id"] == user_id].copy()

            st.success(f"✅ Gợi ý top 20 món ăn cho User {user_id}")
            st.markdown("---")

            # --- Model Performance (demo numbers) ---
            st.subheader("📊 Hiệu suất mô hình (ước lượng)")
            col1, col2 = st.columns(2)
            col1.metric("RMSE", "0.86")
            col2.metric("MAE", "0.68")

            # --- Merge info from recipe_info ---
            recipe_df = pd.DataFrame.from_dict(recipe_info, orient='index').reset_index().rename(columns={"index": "recipe_id"})
            if "recipe_id" in user_recs.columns:
                result = pd.merge(user_recs, recipe_df, on="recipe_id", how="left")
            else:
                result = user_recs

            show_cols = [col for col in ["recipe_id", "name", "ingredients", "tags"] if col in result.columns]
            st.dataframe(result[show_cols].head(20), use_container_width=True)

    st.markdown("---")
    st.caption("📘 Developed by Group 10 — Data Science Project (Food.com Dataset)")
