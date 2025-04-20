import streamlit as st
import pandas as pd

# Đọc dữ liệu từ file Excel
file_path = "GiaDat_HuongHoa_Streamlit.xlsx"
df_khesanh = pd.read_excel(file_path, sheet_name="KHE SANH")
df_laobao = pd.read_excel(file_path, sheet_name="LAO BAO")

# Thiết lập giao diện
st.set_page_config(page_title="Tra cứu giá đất đô thị Hướng Hóa", layout="centered")

# Hiển thị logo + tiêu đề
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.jpg", width=90)
with col2:
    st.title("📍 Tra cứu bảng giá đất – Khe Sanh & Lao Bảo (2025)")

# Chọn khu vực
khu_vuc = st.radio("Chọn khu vực", ["KHE SANH", "LAO BAO"])
df = df_khesanh if khu_vuc == "KHE SANH" else df_laobao

# Kiểm tra đủ dữ liệu
if not df.empty and "Tên đường" in df.columns and "Đoạn đường" in df.columns:

    st.markdown("### 🔍 Nhập tên đường (có thể gõ gần đúng):")
    input_duong = st.text_input("Ví dụ: Hung Vuong, Le Duan...")

    if input_duong:
        ds_duong = df["Tên đường"].dropna().unique().tolist()

        # Tìm các tên đường chứa từ khoá người dùng nhập
        gan_dung = [d for d in ds_duong if input_duong.lower() in d.lower()]

        if gan_dung:
            ten_duong = st.selectbox("📋 Chọn tên đường:", gan_dung)

            # Lấy các đoạn đường ứng với tên đó
            doan_list = df[df["Tên đường"] == ten_duong]["Đoạn đường"].dropna().unique().tolist()
            if doan_list:
                doan_duong = st.selectbox("🚏 Chọn đoạn đường:", doan_list)
            else:
                doan_duong = None

            # Chọn vị trí 1–4
            vi_tri = st.selectbox("📌 Chọn vị trí", ["1", "2", "3", "4"])
            cot_gia = f"Vị trí {vi_tri}"

            # Tìm dòng phù hợp
            if doan_duong:
                row = df[(df["Tên đường"] == ten_duong) & (df["Đoạn đường"] == doan_duong)]
            else:
                row = df[df["Tên đường"] == ten_duong]

            if not row.empty and cot_gia in row.columns:
                loai_duong = row["Loại đường"].values[0]
                gia = row[cot_gia].values[0]
                st.success(
                    f"✅ Giá đất tại **{ten_duong}"
                    + (f" – {doan_duong}" if doan_duong else "")
                    + f"** – loại đường **{loai_duong}** – vị trí **{vi_tri}** là:"
                )
                st.markdown(f"### 💰 **{gia:,} đồng/m²**")
            else:
                st.warning("⚠ Không tìm thấy dữ liệu giá đất phù hợp.")
        else:
            st.warning("❌ Không tìm thấy tên đường chứa từ khóa bạn nhập.")
else:
    st.warning("❌ Dữ liệu thiếu cột 'Tên đường' hoặc 'Đoạn đường'. Vui lòng kiểm tra lại file Excel.")
