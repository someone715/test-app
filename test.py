import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 頁面基本設定
st.set_page_config(page_title="水質監測系統", layout="wide")
st.title("🌊 水質數據監測系統")

# 檔案上傳：支援 csv 和 Excel
uploaded_file = st.file_uploader("請上傳水質數據檔案（CSV 或 Excel）", type=["csv", "xlsx", "xls"])

if uploaded_file:
    # 判斷檔案格式，自動讀取
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 確保日期是文字格式（避免錯誤）
    if "日期" in df.columns:
        df["日期"] = df["日期"].astype(str)
    else:
        st.error("❗️找不到「日期」欄位，請確認資料格式")
        st.stop()

    # 顯示資料表格
    st.subheader("📋 原始資料")
    st.dataframe(df)

    # 使用者選擇欄位
    options = [col for col in df.columns if col != "日期"]
    selected_col = st.selectbox("選擇要繪圖的欄位", options)

    if selected_col:
        # 自動單位對照表
        unit_mapping = {
            "BOD": "mg/L",
            "BOD2": "mg/L",
            "COD": "mg/L",
            "pH": "值",
            "濁度": "NTU",
            "溫度": "°C",
        }

        label = selected_col.strip()
        unit = unit_mapping.get(label, "")
        y_label = f"{label} ({unit})" if unit else label

        # 📈 繪圖
        st.subheader(f"📈 {label} 變化圖")
        fig, ax = plt.subplots()
        ax.plot(df["日期"], df[selected_col], marker='o')
        ax.set_ylabel(y_label)
        ax.set_xlabel("日期")
        ax.tick_params(axis='x', rotation=45)

        # 🔴 異常值（平均 + 2 標準差）
        avg = df[selected_col].mean()
        std = df[selected_col].std()
        outliers = df[selected_col] > avg + 2 * std
        ax.plot(df["日期"][outliers], df[selected_col][outliers], 'ro', label='異常值')
        ax.legend()

        st.pyplot(fig)

        # 顯示統計資訊
        st.info(f"平均值：{avg:.2f}，最大值：{df[selected_col].max():.2f}，最小值：{df[selected_col].min():.2f}")
