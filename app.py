import streamlit as st
import pandas as pd
import os

# 設定資料存檔名稱
FILE_NAME = "inventory.csv"

# 初始化庫存資料 (如果沒有檔案，就建立一個預設的)
def load_data():
    if not os.path.exists(FILE_NAME):
        # 預設一些範例商品
        initial_data = {
            "品號": ["A001", "A002", "P001"],
            "品名": ["iphone", "抗藍光滿版保護貼", "iPhone 15 Pro 256G"],
            "類別": ["配件", "配件", "手機"],
            "庫存數量": [20, 50, 3]
        }
        df = pd.DataFrame(initial_data)
        df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')
    return pd.read_csv(FILE_NAME)

def save_data(df):
    df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')

# --- 網頁介面開始 ---
st.title("📦 門市庫存管理系統")

# 讀取目前庫存
df = load_data()

# 區塊 1：顯示目前庫存狀況
st.header("📍 目前庫存")
# 使用 st.dataframe 讓表格可以在網頁上排序和拉動
st.dataframe(df, use_container_width=True)

st.divider() # 分隔線

# 區塊 2：進出貨操作區
st.header("🔄 庫存異動 (進貨 / 販售)")
col1, col2, col3 = st.columns(3)

with col1:
    # 選擇要異動的商品
    selected_item = st.selectbox("選擇商品", df["品名"].tolist())

with col2:
    # 選擇異動類型
    action = st.radio("動作", ["販售出貨 (-)", "進貨補齊 (+)"])

with col3:
    # 輸入數量
    quantity = st.number_input("數量", min_value=1, value=1, step=1)

# 確認按鈕
if st.button("確認送出"):
    # 找出該商品在表格中的位置
    item_index = df[df["品名"] == selected_item].index[0]
    
    if action == "販售出貨 (-)":
        if df.at[item_index, "庫存數量"] >= quantity:
            df.at[item_index, "庫存數量"] -= quantity
            save_data(df)
            st.success(f"✅ 成功扣除 {quantity} 個 {selected_item}！")
            st.rerun() # 重新整理網頁更新表格
        else:
            st.error("❌ 庫存不足，無法出貨！")
            
    elif action == "進貨補齊 (+)":
        df.at[item_index, "庫存數量"] += quantity
        save_data(df)
        st.success(f"✅ 成功增加 {quantity} 個 {selected_item}！")
        st.rerun()
