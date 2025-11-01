import streamlit as st
import pandas as pd
import pickle, os
import streamlit.components.v1 as components

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Food Recommendation System 🍽️", layout="wide")

# Background image setup
page_bg = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://raw.githubusercontent.com/yourgithubusername/HKN/main/assets/bg_food.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stSidebar"] > div:first-child {{
    background-color: rgba(255, 255, 255, 0.8);
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ------------------ SIDEBAR NAVIGATION ------------------
page = st.sidebar.radio("📖 Chọn trang:", ["EDA Overview", "Recommendation Model"])

# ------------------ PAGE 1: EDA OVERVIEW ------------------
if page == "EDA Overview":
    st.markdown("## 📊 EDA Overview — Tổng quan dữ liệu món ăn")

    st.write("Trang này hiển thị một số thông tin và biểu đồ tổng quan từ dữ liệu gốc (được lưu sẵn dưới dạng ảnh).")

    # ✅ Hiển thị biểu đồ có sẵn trong assets/plots
    plot_dir = "assets/plots"
    plots = {
        "⭐ Phân bố điểm đánh giá": "rating_distribution.png",
        "🍲 Top 10 món ăn phổ biến": "top_recipes.png",
        "🥦 Top 10 nguyên liệu phổ biến": "top_ingredients.png",
        "🔥 Ma trận tương quan dinh dưỡng": "correlation_heatmap.png",
        "💬 Word Cloud – Review người dùng": "wordcloud_reviews.png"
    }

    for title, file in plots.items():
        path = os.path.join(plot_dir, file)
        if os.path.exists(path):
            st.subheader(title)
            st.image(path, use_container_width=True)
        else:
            st.warning(f"⚠️ Không tìm thấy {file}")

    # ✅ Hiển thị biểu đồ động HTML (Plotly)
    html_path = os.path.join(plot_dir, "time_vs_rating_correlation.html")
    if os.path.exists(html_path):
        st.subheader("🕒 Time vs Rating Correlation (Interactive)")
        with open(html_path, "r", encoding="utf-8") as f:
            components.html(f.read(), height=600, scrolling=True)
    else:
        st.info("⚠️ Biểu đồ tương tác chưa được thêm vào thư mục assets/plots.")

# ------------------ PAGE 2: RECOMMENDATION MODEL ------------------
elif page == "Recommendation Model":
    st.markdown("## 🤖 Food Recommendation System")
    st.write("Hệ thống gợi ý món ăn dựa trên lịch sử tương tác người dùng 🍴")

    # Load data
    try:
        with open("data/recommendations.pkl", "rb") as f:
            recommend_df = pickle.load(f)
        if isinstance(recommend_df, dict):
            recommend_df = pd.DataFrame(recommend_df)

        with open("data/recipe_info.pkl", "rb") as f:
            recipe_info = pickle.load(f)
        if isinstance(recipe_info, dict):
            recipe_info = pd.DataFrame(recipe_info)

        # Kiểm tra dữ liệu
        if not {"user_id", "recipe_id"}.issubset(recommend_df.columns):
            st.error("❌ Dữ liệu recommendations.pkl không có cột cần thiết.")
        else:
            model_name = st.selectbox("🔍 Chọn mô hình gợi ý", ["Hybrid SVD", "KNN Basic", "Baseline"])
            user_id = st.number_input("👤 Nhập User ID:", min_value=1, step=1)

            if st.button("🍽️ Gợi ý món ăn"):
                user_recs = recommend_df[recommend_df["user_id"] == user_id].sort_values(by="predicted_rating", ascending=False)
                top_recipes = user_recs.head(5).merge(recipe_info, on="recipe_id", how="left")

                st.success("✅ Các món ăn được đề xuất cho bạn:")
                for _, row in top_recipes.iterrows():
                    st.markdown(f"**🍛 {row['name']}** — ⭐ {row['predicted_rating']:.2f}")
                    if 'image_url' in row and pd.notna(row['image_url']):
                        st.image(row['image_url'], use_container_width=True)

    except Exception as e:
        st.error(f"Lỗi khi load model hoặc dữ liệu: {e}")
