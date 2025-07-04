import streamlit as st
import pandas as pd
import plotly.express as px

# 頁面基本設定
st.set_page_config(page_title="水質監測系統", layout="wide")
st.title("🌊 水質數據監測系統（互動圖表版）")

# 檔案上傳：支援 csv 和 Excel
uploaded_file = st.file_uploader("請上傳水質數據檔案（CSV 或 Excel）", type=["csv", "xlsx", "xls"])

if uploaded_file:
    # 自動讀取格式
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 檢查是否有日期欄位
    if "日期" not in df.columns:
        st.error("❗️找不到「日期」欄位，請確認資料中有『日期』欄")
        st.stop()

    # 日期欄轉換成 datetime 格式
    df["日期"] = pd.to_datetime(df["日期"])

    st.subheader("📋 原始資料")
    st.dataframe(df)

    # 讓使用者選要看的欄位（排除日期）
    options = [col for col in df.columns if col != "日期"]
    selected_col = st.selectbox("選擇要繪圖的欄位", options)

    if selected_col:
        # 自動加上單位
        unit_mapping = {
            "BOD": "mg/L",
            "BOD2": "mg/L",
            "COD": "mg/L",
            "pH": "值",
            "濁度": "NTU",
            "溫度": "°C",
        }
        unit = unit_mapping.get(selected_col.strip(), "")
        y_label = f"{selected_col} ({unit})" if unit else selected_col

        # 異常值：大於平均 + 2 * 標準差
        avg = df[selected_col].mean()
        std = df[selected_col].std()
        df["異常"] = df[selected_col] > avg + 2 * std

        # 建立互動圖表
        fig = px.line(df, x="日期", y=selected_col, title=f"{selected_col} 變化圖",
                      labels={"日期": "日期", selected_col: y_label})

        # 異常值加紅點
        fig.add_scatter(x=df[df["異常"]]["日期"],
                        y=df[df["異常"]][selected_col],
                        mode='markers',
                        marker=dict(color='red', size=10),
                        name='異常值')

        # 顯示圖表
        st.plotly_chart(fig, use_container_width=True)

        # 顯示統計資訊
        st.info(f"📊 平均值：{avg:.2f}，最大值：{df[selected_col].max():.2f}，最小值：{df[selected_col].min():.2f}")
