import streamlit as st
import pandas as pd
import os

FILE_NAME = "inventory.csv"

# 初始化與讀取資料
def load_data():
    if not os.path.exists(FILE_NAME):
        # 【修改點 1】把預設資料改成「完全空白」的格式
        initial_data = {
            "品號": [],
            "品名": [],
            "類別": [],
            "庫存數量": []
        }
        # 強制指定數量欄位為整數型態，避免報錯
        df = pd.DataFrame(initial_data)
        df['庫存數量'] = df['庫存數量'].astype(int)
        df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')
    return pd.read_csv(FILE_NAME)

def save_data(df):
    df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')

st.title("📦 門市庫存管理系統")
df = load_data()

# --- 區塊 1：目前庫存 ---
st.header("📍 目前庫存 (✨可直接點擊表格修改並自動存檔)")
if df.empty:
    st.info("目前倉庫空空如也，請從下方新增商品！")
else:
    # 【新增自動存檔功能】
    # 使用 st.data_editor 取代原本的 st.dataframe，讓表格具備互動性
    edited_df = st.data_editor(df, use_container_width=True, key="inventory_editor")
    
    # 檢查：如果編輯後的資料跟原始載入的資料不一樣，就自動存檔！
    if not edited_df.equals(df):
        save_data(edited_df)
        df = edited_df # 同步更新程式碼裡的 df 變數，確保下方的下拉選單吃到最新資料
        st.toast("💾 變更已自動儲存！", icon="✅") # 畫面右下角跳出輕量提示

st.divider()

# --- 區塊 2：庫存異動 (現有商品進出貨) ---
st.header("🔄 庫存異動")
if not df.empty:
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
else:
    st.warning("請先在下方「新增全新商品」後，才能進行進出貨喔！")

st.divider()

# --- 區塊 3：新增全新商品 ---
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
    if new_id == "" or new_name == "" or new_category == "":
        st.warning("⚠️ 請把品號、品名、類別都填寫完整喔！")
    elif not df.empty and new_name in df["品名"].values:
        st.error("❌ 這個商品名稱已經存在了，請直接在上方做「進貨補齊」！")
    else:
        new_row = pd.DataFrame({
            "品號": [new_id],
            "品名": [new_name],
            "類別": [new_category],
            "庫存數量": [int(new_qty)]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success(f"✅ 成功將 {new_name} 加入庫存系統！")
        st.rerun()

st.divider()

# --- 區塊 4：刪除商品 ---
st.header("🗑️ 刪除商品")
if not df.empty:
    item_to_delete = st.selectbox("選擇要下架/刪除的商品", df["品名"].tolist(), key="delete_select")
    if st.button("❌ 確認刪除此商品"):
        # 【修改點 2】把使用者選到的商品從表格中剔除
        df = df[df["品名"] != item_to_delete]
        save_data(df)
        st.success(f"✅ 已成功刪除 {item_to_delete}！")
        st.rerun()
