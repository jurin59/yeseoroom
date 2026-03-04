import streamlit as st
from PIL import Image
import os

# 1. 페이지 설정
st.set_page_config(page_title="예서의 마법 옷장", layout="centered")

# 스타일 설정: 풍선과 버튼 예쁘게 만들기
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 15px; height: 3.5em; font-size: 1.2rem; }
    .balloon-text { font-size: 2rem; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("💖 예서의 마법 옷장 👗")

# --- 이미지 합성 함수 (아빠가 여기서 숫자를 조절할 수 있어요!) ---
def apply_layer(base_img, path, y_off=20):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            # 모든 이미지를 캐릭터 몸체 크기에 맞춰요
            layer = layer.resize(base_img.size, Image.Resampling.LANCZOS)
            # y_off 값을 조절해서 위아래 위치를 맞출 수 있어요 (예: -20은 위로 이동)
            base_img.alpha_composite(layer, (0, y_off))
    except:
        pass
    return base_img

# --- 파일 목록 가져오기 ---
def get_list(cat):
    items = ["안 함"]
    if os.path.exists(f"{cat}.png"): items.append(cat)
    for i in range(1, 6):
        if os.path.exists(f"{cat}{i}.png"): items.append(f"{cat}{i}")
    return items

# --- 스타일링 메뉴 ---
st.subheader("🎨 예서의 코디 타임")
tab1, tab2, tab3 = st.tabs(["🏠 배경", "💇 헤어/얼굴", "👗 옷/장식"])

with tab1:
    # 깃허브에 '배경1.png', '배경2.png'라고 올리면 목록에 나와요
    bg_list = ["기본 핑크"] + [f"배경{i}" for i in range(1, 5) if os.path.exists(f"배경{i}.png")]
    bg_choice = st.selectbox("어디로 갈까요?", bg_list)

with tab2:
    c1, c2 = st.columns(2)
    with c1: hair_choice = st.selectbox("헤어 스타일", get_list("헤어"))
    with c2: eye_choice = st.selectbox("예쁜 눈", get_list("눈"))
    mouth_choice = st.selectbox("입 모양", get_list("입"))

with tab3:
    style_mode = st.radio("의상 종류", ["한벌", "상하의"], horizontal=True)
    if style_mode == "한벌":
        one_choice = st.selectbox("원피스", get_list("한벌"))
    else:
        c1, c2 = st.columns(2)
        with c1: top_choice = st.selectbox("상의", get_list("상의"))
        with c2: bottom_choice = st.selectbox("하의", get_list("하의"))
    hat_choice = st.selectbox("모자/머리띠", get_list("모자"))

st.divider()

# --- 메인 화면 그리기 ---
try:
    # 1. 배경 설정
    if bg_choice != "기본 핑크" and os.path.exists(f"{bg_choice}.png"):
        canvas = Image.open(f"{bg_choice}.png").convert("RGBA").resize((800, 1200))
    else:
        canvas = Image.new("RGBA", (800, 1200), (255, 242, 245, 255))

    # 2. 캐릭터 몸체
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 3. 아이템 입히기 (순서대로)
        if eye_choice != "안 함": canvas = apply_layer(canvas, f"{eye_choice}.png")
        if mouth_choice != "안 함": canvas = apply_layer(canvas, f"{mouth_choice}.png")
        
        # 헤어가 어색하면 아래 -20 숫자를 0이나 -30으로 바꿔보세요!
        if hair_choice != "안 함": canvas = apply_layer(canvas, f"{hair_choice}.png", y_off=-20)
        
        if style_mode == "한벌" and one_choice != "안 함": 
            canvas = apply_layer(canvas, f"{one_choice}.png")
        elif style_mode == "상하의":
            if top_choice != "안 함": canvas = apply_layer(canvas, f"{top_choice}.png")
            if bottom_choice != "안 함": canvas = apply_layer(canvas, f"{bottom_choice}.png")
            
        if hat_choice != "안 함": canvas = apply_layer(canvas, f"{hat_choice}.png")

        st.image(canvas, use_container_width=True)
    else:
        st.error("body.png 파일을 찾을 수 없어요!")
except Exception as e:
    st.write("이미지를 불러오는 중입니다...")

# --- 풍선 터뜨리기 파티 (클릭하면 팡!) ---
st.divider()
st.subheader("🎈 풍선을 터뜨려요!")

if 'balloons' not in st.session_state:
    st.session_state.balloons = [True] * 5

cols = st.columns(5)
for i in range(5):
    with cols[i]:
        if st.session_state.balloons[i]:
            # 풍선을 누르면 터지는 효과!
            if st.button("🎈", key=f"b_{i}"):
                st.session_state.balloons[i] = False
                st.balloons() # 화면 가득 풍선 축하 효과
                st.rerun()
        else:
            st.markdown("<p class='balloon-text'>💥</p>", unsafe_allow_html=True)

if not any(st.session_state.balloons):
    if st.button("🔄 풍선 다시 불기"):
        st.session_state.balloons = [True] * 5
        st.rerun()

