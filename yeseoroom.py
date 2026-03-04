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
        with c1: top_choice = st.selectbox("상의", get_list("상의"))
        with c2: bottom_choice = st.selectbox("하의", get_list("하의"))
    hat_choice = st.selectbox("모자 및 머리띠", get_list("모자"))

st.divider()

# --- 캐릭터 그리기 영역 ---
try:
    # 1. 배경 설정
    if bg_choice != "기본 핑크" and os.path.exists(f"{bg_choice}.png"):
        canvas = Image.open(f"{bg_choice}.png").convert("RGBA").resize((800, 1200))
    else:
        canvas = Image.new("RGBA", (800, 1200), (255, 242, 245, 255))

    # 2. 몸체(body.png)
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 3. 아이템 겹치기 (눈 -> 입 -> 헤어 -> 옷 -> 모자 순서)
        if eye_choice != "안 함": canvas = apply_layer(canvas, f"{eye_choice}.png")
        if mouth_choice != "안 함": canvas = apply_layer(canvas, f"{mouth_choice}.png")
        
        # 헤어 위치가 안 맞으면 아래 -20 숫자를 조절하세요!
        if hair_choice != "안 함": canvas = apply_layer(canvas, f"{hair_choice}.png", y_off=-20)
        
        if style_mode == "한벌 옷" and one_choice != "안 함": 
            canvas = apply_layer(canvas, f"{one_choice}.png")
        elif style_mode == "상의 & 하의":
            if top_choice != "안 함": canvas = apply_layer(canvas, f"{top_choice}.png")
            if bottom_choice != "안 함": canvas = apply_layer(canvas, f"{bottom_choice}.png")
            
        if hat_choice != "안 함": canvas = apply_layer(canvas, f"{hat_choice}.png")

        st.image(canvas, use_container_width=True)
    else:
        st.error("앗! 깃허브에 'body.png' 사진이 없어요.")
except Exception as e:
    st.write("이미지를 마법으로 불러오는 중... ✨")

# --- 🎈 풍선 터뜨리기 파티 영역 ---
st.divider()
st.subheader("🎈 풍선을 터뜨려요!")

if 'balloons' not in st.session_state:
    st.session_state.balloons = [True] * 5

# 풍선 버튼 5개 가로 배치
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        if st.session_state.balloons[i]:
            if st.button("🎈", key=f"btn_{i}"):
                st.session_state.balloons[i] = False
                st.balloons() # 전체 화면에 축하 풍선이 올라와요!
                st.rerun()
        else:
            st.markdown("<p class='pop-text'>💥</p>", unsafe_allow_html=True)

if not any(st.session_state.balloons):
    if st.button("🔄 풍선 다시 불기"):
        st.session_state.balloons = [True] * 5
        st.rerun()
