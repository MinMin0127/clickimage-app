# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 12:18:59 2025

@author: 00049180
"""


import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
# 設定預設圖片中心座標（可編輯）
st.sidebar.header("Edit Image Center Coordinates")
center_x = st.sidebar.number_input("Center X (µm)", value=202200.123, format="%.3f")
center_y = st.sidebar.number_input("Center Y (µm)", value=150000.11, format="%.3f")
IMAGE_SIZE_UM = 2000  # 2000 x 2000 µm
# 初始化 Streamlit 介面
st.title("📍 DM short term BareWafer Image Click Coordinates")
st.markdown("version 3b by 49180 ")
# 上傳圖片功能
uploaded_files = st.file_uploader("Upload multiple images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
if uploaded_files:
   # 使用 Tab 顯示多張圖片
   tab_options = [f"Image {i+1}" for i in range(len(uploaded_files))]
   selected_image = st.selectbox("Select an image", tab_options)
   # 取得選中的圖片
   image_index = tab_options.index(selected_image)
   image = Image.open(uploaded_files[image_index])
   # 確保 session state 存在
   if "click_data" not in st.session_state:
       st.session_state.click_data = {}
   if "click_positions" not in st.session_state:
       st.session_state.click_positions = {}
   # 提示點擊的圖片
   st.subheader(f"📌 Tap on {selected_image} below")
   from streamlit_image_coordinates import streamlit_image_coordinates
   coords = streamlit_image_coordinates(image, key=f"click_image_{image_index}")
   if coords:
       x_pixel, y_pixel = coords["x"], coords["y"]
       new_click = (x_pixel, y_pixel)
       if image_index not in st.session_state.click_positions:
           st.session_state.click_positions[image_index] = []
       if image_index not in st.session_state.click_data:
           st.session_state.click_data[image_index] = []
       if new_click not in st.session_state.click_positions[image_index]:
           # 計算 µm 座標
           x_um = center_x + (x_pixel - image.width / 2) * (IMAGE_SIZE_UM / image.width)
           y_um = center_y - (y_pixel - image.height / 2) * (IMAGE_SIZE_UM / image.height)
           # 存入點擊座標
           st.session_state.click_data[image_index].append((x_um, y_um))
           st.session_state.click_positions[image_index].append(new_click)
   # 在圖片上標示點擊位置（紅色叉叉與點擊順序）
   draw = ImageDraw.Draw(image)
   for i, pos in enumerate(st.session_state.click_positions.get(image_index, [])):
       x, y = pos
       draw.line([(x-10, y-10), (x+10, y+10)], fill="red", width=3)
       draw.line([(x+10, y-10), (x-10, y+10)], fill="red", width=3)
       draw.text((x+12, y), f"{i+1}st tap", fill="red")
   # 標記圖片中心點（紅色圓圈）
   center_x_pixel = image.width // 2
   center_y_pixel = image.height // 2
   draw.ellipse([(center_x_pixel-5, center_y_pixel-5), (center_x_pixel+5, center_y_pixel+5)], outline="red", width=2)
   draw.text((center_x_pixel+10, center_y_pixel-10), "Center", fill="red")
   # 顯示標記後的圖片
   st.subheader(f"✅ Check the points you tapped on {selected_image}")
   st.image(image, caption=f"📌 {selected_image} with Tap Coordinates", use_column_width=True)
   # 顯示已記錄座標
   if st.session_state.click_data.get(image_index):
       df = pd.DataFrame(st.session_state.click_data[image_index], columns=["X (µm)", "Y (µm)"])
       st.write(f"### Clicked Coordinates for {selected_image}")
       st.dataframe(df)
   # 清除座標按鈕
   if st.button(f"Clear Coordinates for {selected_image}"):
       st.session_state.click_data[image_index] = []
       st.session_state.click_positions[image_index] = []
       st.success(f"✅ Coordinates cleared for {selected_image}.")
else:
   st.warning("⚠ Please upload some images to proceed.")


