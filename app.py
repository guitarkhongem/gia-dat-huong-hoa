import streamlit as st
import pandas as pd
from difflib import get_close_matches

file_path = "GiaDat_HuongHoa_Streamlit.xlsx"
df_khesanh = pd.read_excel(file_path, sheet_name="KHE SANH")
df_laobao = pd.read_excel(file_path, sheet_name="LAO BAO")

# Cấu hình trang
st.set_page_config(page_title="Tra cứu giá đất đô thị Hướng Hóa", layout="centered")

# 👉 Hiển thị logo bên trái, tiêu đề bên phải
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.jpg", width=90)
with col2:
    st.title("📍 Tra cứu bảng giá đất – Khe Sanh & Lao Bảo (2025)")

# Chọn khu vực
khu_vuc = st.radio("Chọn khu vực", ["KHE SANH", "LAO BAO"])
df = df_khesanh if khu_vuc == "KHE SANH" else df_laobao

# Tra cứu tên đường
if not df.empty and "Tên đường" in df.columns:
    st.markdown("### 🔍 Nhập tên đường (có thể gõ gần đúng):")
    input_duong = st.text_input("Ví dụ: Hung Vuong, Le Duan...")

    if input_duong:
        ds_duong = df["Tên đường"].dropna().unique().tolist()
        gan_dung = get_close_matches(input_duong, ds_duong, n=3, cutoff=0.4)

        if gan_dung:
            ten_duong = st.selectbox("📋 Chọn tên gần đúng:", gan_dung)
            vi_tri = st.selectbox("📌 Chọn vị trí", ["1", "2", "3", "4"])
            cot_gia = f"Vị trí {vi_tri}"

            row = df[df["Tên đường"] == ten_duong]
            if not row.empty and cot_gia in row.columns:
                loai_duong = row["Loại đường"].values[0]
                gia = row[cot_gia].values[0]
                st.success(f"✅ Giá đất tại **{ten_duong}** – loại đường **{loai_duong}** – vị trí **{vi_tri}** là:")
                st.markdown(f"### 💰 **{gia:,} đồng/m²**")
        else:
            st.warning("❌ Không tìm thấy tên đường gần đúng.")
else:
    st.warning("❌ Dữ liệu không hợp lệ hoặc thiếu cột 'Tên đường'.")
