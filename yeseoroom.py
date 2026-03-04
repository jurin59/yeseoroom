import streamlit as st
from PIL import Image
import os
import random

# 1. 페이지 설정
st.set_page_config(page_title="예서의 마법 옷장", layout="centered", initial_sidebar_state="collapsed")

# 2. 풍선 애니메이션 및 스타일 (CSS)
st.markdown("""
    <style>
    @keyframes floatUp {
        0% { transform: translateY(100vh); opacity: 1; }
        100% { transform: translateY(-100vh); opacity: 0.8; }
    }
    .balloon-btn {
        font-size: 40px !important;
        background: none !important;
        border: none !important;
        animation: floatUp 5s linear infinite;
        position: fixed;
        bottom: -50px;
    }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.title("💖 예서의 무한 변신 옷장 👗")

# --- 이미지 합성 엔진 (자동 위치 맞춤) ---
def apply_layer(base_img, path, y_offset=0):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            # 아이템이 몸체보다 작을 경우, 중앙에 배치하도록 계산
            bg_w, bg_h = base_img.size
            l_w, l_h = layer.size
            
            # 비율 유지하며 너비 맞추기
            ratio = bg_w / l_w
            layer = layer.resize((bg_w, int(l_h * ratio)), Image.Resampling.LANCZOS)
            
            # 합성 (중앙 기준, y_offset으로 상하 조절)
            base_img.alpha_composite(layer, (0, y_offset))
    except:
        pass
    return base_img

# --- 메뉴 구성 ---
def get_list(cat):
    items = ["안 함"]
    if os.path.exists(f"{cat}.png"): items.append(cat)
    for i in range(1, 6):
        if os.path.exists(f"{cat}{i}.png"): items.append(f"{cat}{i}")
    return items

tabs = st.tabs(["🏠 배경", "💇 헤어/눈", "👗 의상", "🎀 장식"])

with tabs[0]:
    # 배경 리스트 자동 인식 (bg1, bg2 등)
    bg_list = ["기본 핑크"] + [f"배경{i}" for i in range(1, 5) if os.path.exists(f"배경{i}.png")]
    bg_choice = st.selectbox("어디로 갈까요?", bg_list)

with tabs[1]:
    c1, c2 = st.columns(2)
    with c1: hair_choice = st.selectbox("헤어 스타일", get_list("헤어"))
    with c2: eye_choice = st.selectbox("예쁜 눈", get_list("눈"))
    mouth_choice = st.selectbox("입 모양", get_list("입"))

with tabs[2]:
    mode = st.radio("의상 종류", ["한벌", "상하의"], horizontal=True)
    if mode == "한벌":
        one_choice = st.selectbox("원피스", get_list("한벌"))
    else:
        c1, c2 = st.columns(2)
        with c1: top_choice = st.selectbox("상의", get_list("상의"))
        with c2: bottom_choice = st.selectbox("하의", get_list("하의"))

with tabs[3]:
    hat_choice = st.selectbox("모자/머리띠", get_list("모자"))
    acc_choice = st.selectbox("기타 장식", get_list("악세사리"))

# --- 메인 캔버스 생성 ---
try:
    # 1. 배경 (파일명이 '배경1.png' 형태여야 함)
    bg_path = f"{bg_choice}.png"
    if bg_choice != "기본 핑크" and os.path.exists(bg_path):
        canvas = Image.open(bg_path).convert("RGBA").resize((800, 1200))
    else:
        canvas = Image.new("RGBA", (800, 1200), (255, 242, 245, 255))

    # 2. 몸체
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 3. 레이어 합성 (순서 중요)
        if eye_choice != "안 함": canvas = apply_layer(canvas, f"{eye_choice}.png")
        if mouth_choice != "안 함": canvas = apply_layer(canvas, f"{mouth_choice}.png")
        # 헤어는 약간 위로 보정 (-20 정도)
        if hair_choice != "안 함": canvas = apply_layer(canvas, f"{hair_choice}.png", y_offset=-20)
        
        if mode == "한벌" and one_choice != "안 함": 
            canvas = apply_layer(canvas, f"{one_choice}.png")
        elif mode == "상하의":
            if top_choice != "안 함": canvas = apply_layer(canvas, f"{top_choice}.png")
            if bottom_choice != "안 함": canvas = apply_layer(canvas, f"{bottom_choice}.png")
            
        if hat_choice != "안 함": canvas = apply_layer(canvas, f"{hat_choice}.png")
        if acc_choice != "안 함": canvas = apply_layer(canvas, f"{acc_choice}.png")

        st.image(canvas, use_container_width=True)
    else:
        st.error("body.png 파일이 필요해요!")
except Exception as e:
    st.write("이미지를 불러오는 중이에요...")

# --- 떠오르는 풍선 터뜨리기 파티 ---
st.divider()
st.subheader("🎈 떠오르는 풍선을 터뜨려봐!")

if 'pop_count' not in st.session_state: st.session_state.pop_count = 0

# 가로로 나열된 풍선 버튼들 (애니메이션 느낌만 제공)
b_cols = st.columns(5)
for i in range(5):
    with b_cols[i]:
        if st.button("🎈", key=f"fly_b_{i}"):
            st.session_state.pop_count += 1
            st.balloons() # 터질 때 팡 터지는 효과

st.write(f"✨ 예서가 터뜨린 풍선: {st.session_state.pop_count}개")
