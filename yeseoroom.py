import streamlit as st
from PIL import Image
import os

# 1. 페이지 설정
st.set_page_config(page_title="예서의 마법 옷장", layout="centered", initial_sidebar_state="collapsed")

# 스타일 설정
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; }
    .category-box { background-color: #FFF0F5; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💖 예서의 무한 변신 옷장 👗")

# --- 이미지 합성 함수 ---
def apply_layer(base_img, path):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            base_img.alpha_composite(layer.resize(base_img.size))
    except:
        pass
    return base_img

# --- 파일 존재 확인 및 리스트 생성 함수 ---
def get_item_list(category_name):
    # 번호 없는 기본 파일 확인
    items = []
    if os.path.exists(f"{category_name}.png"):
        items.append(category_name)
    # 1번부터 4번까지 확인
    for i in range(1, 5):
        if os.path.exists(f"{category_name}{i}.png"):
            items.append(f"{category_name}{i}")
    return ["안 함"] + items

# --- 조작 영역 ---
st.subheader("🎨 예서의 스타일링 센터")
tabs = st.tabs(["🏠 배경", "💇 헤어/눈", "👗 의상", "🎀 액세서리"])

with tabs[0]:
    bg_choice = st.selectbox("어디로 갈까요?", ["기본 배경", "핑크 방", "푸른 공원"])

with tabs[1]:
    col1, col2 = st.columns(2)
    with col1:
        hair_choice = st.selectbox("헤어 스타일", get_item_list("헤어"))
    with col2:
        eye_choice = st.selectbox("예쁜 눈", get_item_list("눈"))

with tabs[2]:
    style_mode = st.radio("의상 종류", ["한벌 옷", "상의 & 하의"], horizontal=True)
    if style_mode == "한벌 옷":
        onepiece_choice = st.selectbox("한벌 코디", get_item_list("한벌"))
        top_choice, bottom_choice = "안 함", "안 함"
    else:
        c1, c2 = st.columns(2)
        with c1: top_choice = st.selectbox("상의", get_item_list("상의"))
        with c2: bottom_choice = st.selectbox("하의", get_item_list("하의"))
        onepiece_choice = "안 함"

with tabs[3]:
    c1, c2 = st.columns(2)
    with c1:
        hat_choice = st.selectbox("모자", get_item_list("모자"))
    with c2:
        mouth_choice = st.selectbox("입 모양", get_item_list("입"))

# --- 이미지 생성 및 출력 ---
try:
    # 배경 생성
    bg_file = "bg1.png" if bg_choice == "핑크 방" else "bg2.png" if bg_choice == "푸른 공원" else None
    if bg_file and os.path.exists(bg_file):
        canvas = Image.open(bg_file).convert("RGBA").resize((800, 1200))
    else:
        canvas = Image.new("RGBA", (800, 1200), (255, 245, 250, 255))

    # 캐릭터 베이스
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 레이어 순서대로 입히기 (눈 -> 헤어 -> 옷 -> 모자 순)
        if eye_choice != "안 함": canvas = apply_layer(canvas, f"{eye_choice}.png")
        if mouth_choice != "안 함": canvas = apply_layer(canvas, f"{mouth_choice}.png")
        if hair_choice != "안 함": canvas = apply_layer(canvas, f"{hair_choice}.png")
        
        # 옷 입히기
        if style_mode == "한벌 옷":
            if onepiece_choice != "안 함": canvas = apply_layer(canvas, f"{onepiece_choice}.png")
        else:
            if top_choice != "안 함": canvas = apply_layer(canvas, f"{top_choice}.png")
            if bottom_choice != "안 함": canvas = apply_layer(canvas, f"{bottom_choice}.png")
            
        if hat_choice != "안 함": canvas = apply_layer(canvas, f"{hat_choice}.png")

        st.image(canvas, use_container_width=True)
    else:
        st.warning("body.png 파일을 찾을 수 없어요!")

except Exception as e:
    st.error("이미지를 합성하는 중 에러가 났어요. 파일 이름을 확인해 주세요!")

# --- 풍선 터뜨리기 게임 ---
st.divider()
st.subheader("🎈 풍선 터뜨리기 파티!")
if 'balloons' not in st.session_state:
    st.session_state.balloons = [True] * 5

b_cols = st.columns(5)
for i in range(5):
    with b_cols[i]:
        if st.session_state.balloons[i]:
            if st.button("🎈", key=f"b_{i}"):
                st.session_state.balloons[i] = False
                st.rerun()
        else: st.write("💥")

if not any(st.session_state.balloons):
    if st.button("🔄 풍선 다시 불기"):
        st.session_state.balloons = [True] * 5
        st.rerun()
