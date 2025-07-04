import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="水質監測系統", layout="wide")
st.title("🌊 水質數據監測系統")

uploaded_file = st.file_uploader("請上傳水質數據檔案(CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 原始資料")
    st.dataframe(df)

    # 可選欄位
    options = df.columns.tolist()
    selected_col = st.selectbox("選擇要繪圖的欄位", options)

    if selected_col:
        st.subheader(f"📈 {selected_col} 變化圖")
        fig, ax = plt.subplots()
        ax.plot(df[selected_col], marker='o')
        ax.set_ylabel(selected_col)
        ax.set_xlabel("資料點")
        
        # 異常提示：大於平均+2倍標準差
        avg = df[selected_col].mean()
        std = df[selected_col].std()
        outliers = df[selected_col] > avg + 2 * std
        ax.plot(df[selected_col][outliers], 'ro', label='異常值')
        ax.legend()

        st.pyplot(fig)

        st.info(f"平均值：{avg:.2f}，最大值：{df[selected_col].max():.2f}，最小值：{df[selected_col].min():.2f}")
