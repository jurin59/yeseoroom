import streamlit as st
from PIL import Image
import os

# 1. 페이지 설정
st.set_page_config(page_title="예서의 마법 옷장", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stSlider { padding-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3em; background-color: #FFB6C1; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("💖 예서의 무한 변신 옷장 👗")

# --- 이미지 합성 함수 (위치/크기 조절 기능 추가) ---
def apply_layer(base_img, path, x_off=0, y_off=0, scale=1.0):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            # 1. 크기 조절 (기본 너비에 scale 곱하기)
            bg_w, bg_h = base_img.size
            new_w = int(bg_w * scale)
            new_h = int(layer.size[1] * (new_w / layer.size[0]))
            layer = layer.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # 2. 합성 (x_off, y_off 적용)
            # 기본 중앙 배치를 위해 좌측 여백 계산
            start_x = (bg_w - new_w) // 2 + x_off
            base_img.alpha_composite(layer, (start_x, y_off))
    except:
        pass
    return base_img

# --- 파일 목록 인식 ---
def get_list(cat):
    items = ["안 함"]
    if os.path.exists(f"{cat}.png"): items.append(cat)
    for i in range(1, 6):
        if os.path.exists(f"{cat}{i}.png"): items.append(f"{cat}{i}")
    return items

# --- 메뉴 구성 ---
with st.sidebar:
    st.header("🛠️ 마법 조절 도구")
    edit_mode = st.checkbox("아이템 크기/위치 조절하기")
    if edit_mode:
        st.info("아래 슬라이더로 위치를 맞춘 뒤 숫자를 기억하세요!")
        adj_x = st.slider("가로 이동", -400, 400, 0)
        adj_y = st.slider("세로 이동", -200, 800, 0)
        adj_s = st.slider("크기 조절", 0.1, 2.0, 1.0, 0.05)
    else:
        adj_x, adj_y, adj_s = 0, 0, 1.0

tabs = st.tabs(["🏠 배경", "💇 헤어/눈", "👗 의상", "🎀 장식"])

with tabs[0]:
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

# --- 메인 캔버스 그리기 ---
try:
    # 배경
    bg_path = f"{bg_choice}.png"
    if bg_choice != "기본 핑크" and os.path.exists(bg_path):
        canvas = Image.open(bg_path).convert("RGBA").resize((800, 1200))
    else:
        canvas = Image.new("RGBA", (800, 1200), (255, 242, 245, 255))

    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 아이템 합성 (조절 모드일 때는 마지막에 선택한 카테고리에 슬라이더 값이 적용됨)
        # 평소에는 기본값(0, 0, 1.0)으로 작동
        
        # 순서대로 입히기
        if eye_choice != "안 함": canvas = apply_layer(canvas, f"{eye_choice}.png")
        if mouth_choice != "안 함": canvas = apply_layer(canvas, f"{mouth_choice}.png")
        
        # 헤어 조절 예시 (조절 모드 켜졌을 때 헤어 탭이면 작동)
        h_x, h_y, h_s = (adj_x, adj_y, adj_s) if edit_mode and hair_choice != "안 함" else (0, -20, 1.0)
        if hair_choice != "안 함": canvas = apply_layer(canvas, f"{hair_choice}.png", h_x, h_y, h_s)
        
        if mode == "한벌" and one_choice != "안 함": canvas = apply_layer(canvas, f"{one_choice}.png")
        elif mode == "상하의":
            if top_choice != "안 함": canvas = apply_layer(canvas, f"{top_choice}.png")
            if bottom_choice != "안 함": canvas = apply_layer(canvas, f"{bottom_choice}.png")
            
        if hat_choice != "안 함": canvas = apply_layer(canvas, f"{hat_choice}.png")
        if acc_choice != "안 함": canvas = apply_layer(canvas, f"{acc_choice}.png")

        st.image(canvas, use_container_width=True)
        
        if edit_mode:
            st.warning(f"현재 조절 값 -> 가로: {adj_x}, 세로: {adj_y}, 크기: {adj_s}")
    else:
        st.error("body.png 파일이 필요해요!")
except Exception as e:
    st.write("이미지 로딩 중...")

# --- 풍선 파티 ---
st.divider()
if 'balloons' not in st.session_state: st.session_state.balloons = [True] * 5
b_cols = st.columns(5)
for i in range(5):
    with b_cols[i]:
        if st.session_state.balloons[i]:
            if st.button("🎈", key=f"b_{i}"):
                st.session_state.balloons[i] = False
                st.rerun()
        else: st.write("💥")
