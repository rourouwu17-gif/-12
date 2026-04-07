import streamlit as st
import pandas as pd
import os

FILE_NAME = "inventory.csv"

# 初始化與讀取資料
def load_data():
    if not os.path.exists(FILE_NAME):
        initial_data = {
            "品號": ["A001", "A002", "P001"],
            "品名": ["20W PD 快充頭", "抗藍光滿版保護貼", "iPhone 15 Pro 256G"],
            "類別": ["配件", "配件", "手機"],
            "庫存數量": [20, 50, 3]
        }
        df = pd.DataFrame(initial_data)
        df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')
    return pd.read_csv(FILE_NAME)

def save_data(df):
    df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')

st.title("📦 門市庫存管理系統")
df = load_data()

# 區塊 1：目前庫存
st.header("📍 目前庫存")
st.dataframe(df, use_container_width=True)

st.divider()

# 區塊 2：庫存異動 (針對現有商品)
st.header("🔄 庫存異動 (現有商品進出貨)")
col1, col2, col3 = st.columns(3)

with col1:
    selected_item = st.selectbox("選擇現有商品", df["品名"].tolist())
with col2:
    action = st.radio("動作", ["販售出貨 (-)", "進貨補齊 (+)"])
with col3:
    quantity = st.number_input("數量", min_value=1, value=1, step=1)

if st.button("確認異動"):
    item_index = df[df["品名"] == selected_item].index[0]
    if action == "販售出貨 (-)":
        if df.at[item_index, "庫存數量"] >= quantity:
            df.at[item_index, "庫存數量"] -= quantity
            save_data(df)
            st.success(f"✅ 成功扣除 {quantity} 個 {selected_item}！")
            st.rerun()
        else:
            st.error("❌ 庫存不足，無法出貨！")
    elif action == "進貨補齊 (+)":
        df.at[item_index, "庫存數量"] += quantity
        save_data(df)
        st.success(f"✅ 成功增加 {quantity} 個 {selected_item}！")
        st.rerun()

st.divider()

# 區塊 3：新增全新商品 (你要求的新功能！)
st.header("🆕 新增全新商品")
col_new1, col_new2 = st.columns(2)
col_new3, col_new4 = st.columns(2)

with col_new1:
    new_id = st.text_input("輸入品號 (例如：C001)")
with col_new2:
    new_name = st.text_input("輸入新品名 (例如：Type-C 編織線)")
with col_new3:
    new_category = st.text_input("輸入類別 (例如：配件)")
with col_new4:
    new_qty = st.number_input("初始進貨數量", min_value=0, value=0, step=1)

if st.button("➕ 確認新增這項商品"):
    # 檢查有沒有漏填
    if new_id == "" or new_name == "" or new_category == "":
        st.warning("⚠️ 請把品號、品名、類別都填寫完整喔！")
    # 檢查是否已經有重複的品名
    elif new_name in df["品名"].values:
        st.error("❌ 這個商品名稱已經存在了，請直接在上方做「進貨補齊」！")
    else:
        # 把新商品打包成一行資料
        new_row = pd.DataFrame({
            "品號": [new_id],
            "品名": [new_name],
            "類別": [new_category],
            "庫存數量": [new_qty]
        })
        # 把新資料接到舊資料的最下面
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success(f"✅ 成功將 {new_name} 加入庫存系統！")
        st.rerun()
