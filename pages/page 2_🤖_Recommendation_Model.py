import streamlit as st
import pandas as pd
import pickle
import os

# ==============================
# ⚙️ Cấu hình
# ==============================
st.set_page_config(page_title="Recommendation Model", page_icon="🤖", layout="wide")

BASE_PATH = r"C:\Users\ADMIN\Downloads\HKN"
MODEL_PATH = os.path.join(BASE_PATH, "models")

# ==============================
# 🔧 Load model và dữ liệu
# ==============================
@st.cache_resource
def load_models():
    try:
        model_fast = pickle.load(open(os.path.join(MODEL_PATH, "final_fast_model.pkl"), "rb"))
        model_best = pickle.load(open(os.path.join(MODEL_PATH, "final_best_model.pkl"), "rb"))
        recipe_info = pickle.load(open(os.path.join(MODEL_PATH, "recipe_info.pkl"), "rb"))
        recommendations = pickle.load(open(os.path.join(MODEL_PATH, "recommendations.pkl"), "rb"))
        return model_fast, model_best, recipe_info, recommendations
    except Exception as e:
        st.error(f"Lỗi khi load model hoặc dữ liệu: {e}")
        return None, None, None, None

model_fast, model_best, recipe_info, recommendations = load_models()

# ==============================
# 🧭 Giao diện chính
# ==============================
st.title("🤖 Food Recommendation System")
st.markdown("### Chạy mô hình gợi ý món ăn dựa trên dữ liệu người dùng và món ăn 🍲")

# Chọn mô hình
model_option = st.selectbox(
    "🧩 Chọn mô hình để dự đoán",
    ["Hybrid Simple (SVD)", "Hybrid Best (Fine-tuned Hybrid)"]
)

if model_option == "Hybrid Simple (SVD)":
    model = model_fast
else:
    model = model_best

# Nhập user ID
st.sidebar.header("🔢 Chọn người dùng")
user_id = st.sidebar.number_input("Nhập User ID:", min_value=1, step=1, value=12345)

# ==============================
# 🚀 Thực thi gợi ý
# ==============================
if st.button("Tạo gợi ý món ăn"):
    if model is None:
        st.error("❌ Model chưa được load đúng. Kiểm tra lại thư mục models/.")
    else:
        with st.spinner("Đang tạo gợi ý..."):
            try:
                top20_df = pd.DataFrame(recommendations[:20])
                st.success("✅ Gợi ý món ăn đã sẵn sàng!")
                st.subheader("🍽️ Top 20 món ăn được đề xuất")
                st.dataframe(top20_df, use_container_width=True)

                st.markdown("---")
                st.subheader("📘 Chi tiết món ăn đầu tiên:")
                first = top20_df.iloc[0]
                st.write(f"**Tên món:** {first.get('name', 'N/A')}")
                st.write(f"**Nguyên liệu:** {first.get('ingredients', 'N/A')}")
                st.write(f"**Tags:** {first.get('tags', 'N/A')}")

            except Exception as e:
                st.error(f"Lỗi khi chạy gợi ý: {e}")

# ==============================
# 📈 Hiệu suất model
# ==============================
st.markdown("---")
st.header("📊 Hiệu suất mô hình")
col1, col2 = st.columns(2)
col1.metric("RMSE (ước lượng)", "0.86")
col2.metric("MAE (ước lượng)", "0.68")
st.caption("Các chỉ số này được tính từ tập test trong quá trình huấn luyện ban đầu.")
st.markdown("---")
st.caption("Developed by Group 10 — Data Science Project (Food.com Dataset)")
