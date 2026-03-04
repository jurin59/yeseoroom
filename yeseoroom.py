import streamlit as st
from PIL import Image
import os

# 1. 버전 정보 및 페이지 설정
VERSION = "v1.2 (2026-03-04)"
st.set_page_config(page_title=f"예서의 마법 옷장 {VERSION}", layout="centered")

# 디자인 설정 (CSS)
st.markdown(f"""
    <style>
    .version-tag {{ color: #FF69B4; font-weight: bold; text-align: right; font-size: 0.8rem; }}
    .stButton>button {{ width: 100%; border-radius: 15px; height: 3.5em; font-size: 1.2rem; background-color: #FFF0F5; }}
    .pop-text {{ font-size: 2.5rem; text-align: center; }}
    </style>
    <div class="version-tag">업데이트 버전: {VERSION}</div>
    """, unsafe_allow_html=True)

st.title("💖 예서의 마법 옷장 👗")

# --- 이미지 합성 함수 (위치 보정 기능 포함) ---
def apply_layer(base_img, path, y_off=0):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            # 모든 레이어 크기를 몸체와 똑같이 맞춤
            layer = layer.resize(base_img.size, Image.Resampling.LANCZOS)
            # y_off: 숫자가 작을수록(예: -30) 위로, 클수록 아래로 이동
            base_img.alpha_composite(layer, (0, y_off))
    except:
        pass
    return base_img

# --- 파일 목록 자동 생성 ---
def get_list(cat):
    items = ["안 함"]
    if os.path.exists(f"{cat}.png"): items.append(cat)
    for i in range(1, 6):
        if os.path.exists(f"{cat}{i}.png"): items.append(f"{cat}{i}")
    return items

# --- 스타일링 메뉴 ---
st.subheader("🎨 예서의 코디 타임")
tab1, tab2, tab3 = st.tabs(["🏠 배경 선택", "💇 얼굴/헤어", "👗 의상/모자"])

with tab1:
    # 깃허브에 '배경1.png', '배경2.png'라고 올리면 자동으로 목록에 떠요
    bg_list = ["기본 핑크"] + [f"배경{i}" for i in range(1, 6) if os.path.exists(f"배경{i}.png")]
    bg_choice = st.selectbox("어디로 놀러 갈까요?", bg_list)

with tab2:
    c1, c2 = st.columns(2)
    with c1: hair_choice = st.selectbox("헤어 스타일", get_list("헤어"))
    with c2: eye_choice = st.selectbox("예쁜 눈", get_list("눈"))
    mouth_choice = st.selectbox("입 모양", get_list("입"))

with tab3:
    style_mode = st.radio("의상 종류", ["한벌 옷", "상의 & 하의"], horizontal=True)
    if style_mode == "한벌 옷":
        one_choice = st.selectbox("원피스/드레스", get_list("한벌"))
    else:
        c1, c2 = st.columns(2)
