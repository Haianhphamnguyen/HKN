import streamlit as st
import pickle
import base64
from pathlib import Path

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="HKN - Recipe Recommender",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------ HELPERS ------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

ASSETS = Path("assets")
DATA = Path("data")

bg_path = ASSETS / "bg_food.jpg"
bg_img = get_base64_image(bg_path) if bg_path.exists() else None

# ------------------ BACKGROUND CSS ------------------
st.markdown(f"""
<style>
.stApp {{
    {f'background-image: url("data:image/jpg;base64,{bg_img}");' if bg_img else ''}
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.app-overlay {{
    position: fixed;
    inset: 0;
    background: rgba(255, 255, 255, 0.75);
    z-index: 0;
}}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="app-overlay"></div>', unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
@st.cache_resource
def load_pickles():
    try:
        with open(DATA / "recommendations.pkl", "rb") as f:
            recs = pickle.load(f)
    except Exception as e:
        st.error(f"Lỗi khi đọc recommendations.pkl: {e}")
        recs = {}
    try:
        with open(DATA / "light_recipe_info.pkl", "rb") as f:
            info = pickle.load(f)
    except Exception as e:
        st.error(f"Lỗi khi đọc recipe_info.pkl: {e}")
        info = {}
    return recs, info

recs, recipe_info = load_pickles()

# ------------------ HEADER ------------------
st.markdown("""
<div style='background:linear-gradient(135deg,#667eea,#764ba2,#f093fb);
            padding:1.5rem;border-radius:15px;text-align:center;color:white;'>
    <h1>🍳 HKN - Recipe Recommender System</h1>
    <p>Personalized Recommendations using Hybrid SVD + CBF</p>
</div>
""", unsafe_allow_html=True)

# ------------------ TABS ------------------
tab1, tab2 = st.tabs(["📊 EDA & Data Overview", "🤖 Model Recommendation"])

# ------------------ PAGE 1: EDA ------------------
with tab1:
    st.subheader("📈 Tổng quan Dữ liệu")

    # Thông tin mô tả dữ liệu (nếu có file JSON summary)
    json_path = DATA / "eda_summary.json"
    if json_path.exists():
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            eda_info = json.load(f)
        st.json(eda_info)
    else:
        st.info("⚠️ Không có file eda_summary.json, chỉ hiển thị biểu đồ trong assets")

    # Biểu đồ EDA
    st.markdown("### 🔍 Phân tích Hình ảnh EDA")
    eda_images = [
        ("eda_rating_distribution.png", "Phân bố điểm đánh giá"),
        ("eda_Ratings_per_Recipe.png", "Số lượt đánh giá mỗi công thức"),
        ("eda_Average Rating vs Number of Ingredients.png", "Số nguyên liệu vs Rating"),
        ("eda_Word Cloud for Ingredients.png", "Từ khóa nguyên liệu phổ biến"),
        ("eda_Word Cloud for Tags.png", "Từ khóa tags phổ biến"),
    ]

    cols = st.columns(2)
    for i, (img_name, caption) in enumerate(eda_images):
        path = ASSETS / img_name
        if path.exists():
            with cols[i % 2]:
                st.image(str(path), caption=caption, use_container_width=True)
        else:
            st.warning(f"Thiếu file: {img_name}")

# ------------------ PAGE 2: MODEL ------------------
with tab2:
    st.subheader("⚙️ Chọn Model & User")

    if not recs:
        st.error("❌ Không tải được dữ liệu recommendations.pkl")
    elif not recipe_info:
        st.error("❌ Không tải được dữ liệu recipe_info.pkl")
    else:
        model_choice = st.selectbox(
            "Chọn Model",
            ["Hybrid Simple (α=0.9 SVD)", "Hybrid CBF (α=0.7 SVD + 0.3 CBF)"]
        )
        model_key = 'fast' if "Simple" in model_choice else 'best'

        try:
            users = sorted(list(recs[model_key].keys()))[:10]
        except Exception:
            st.error("Không tìm thấy danh sách user trong dữ liệu!")
            users = []

        if users:
            user_id = st.selectbox("Chọn User ID", users)
            if st.button("🎯 Recommend Top-20", use_container_width=True):
                try:
                    top20 = recs[model_key][user_id]
                    st.write("✅ Hiển thị gợi ý cho user:", user_id)
                    cols = st.columns(4)
                    for i, rid in enumerate(top20):
                        if rid in recipe_info:
                            with cols[i % 4]:
                                info = recipe_info[rid]
                                name = info.get('name', f"Recipe {rid}")
                                tags = ", ".join(info.get('tags', [])[:3])
                                st.markdown(f"""
                                <div style='background:white;border-radius:12px;
                                            padding:1rem;margin-bottom:1rem;
                                            box-shadow:0 3px 10px rgba(0,0,0,0.1);'>
                                    <h4 style='margin:0;color:#333;'>{name}</h4>
                                    <p style='margin:0.2rem 0 0;font-size:0.9rem;color:#666;'>ID: {rid}</p>
                                    <p style='margin:0.2rem 0 0;font-size:0.85rem;color:#FF6B6B;'>Tags: {tags}</p>
                                </div>
                                """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Lỗi khi hiển thị gợi ý: {e}")

# ------------------ FOOTER ------------------
st.markdown("""
<div style='text-align:center;margin-top:2rem;font-size:0.9rem;color:#555;'>
    <p><strong>HKN - Data Science Project 2025</strong></p>
    <p><em>Hybrid Recommendation System using SVD + CBF</em></p>
</div>
""", unsafe_allow_html=True)
