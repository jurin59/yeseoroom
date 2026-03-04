import streamlit as st
from PIL import Image
import os

# 1. 페이지 설정 (모바일 및 태블릿 최적화)
st.set_page_config(page_title="예서의 마법 옷장", layout="centered", initial_sidebar_state="collapsed")

# 스타일 설정: 모바일 터치 편의성 향상
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #FFB6C1; color: white; font-weight: bold; }
    .stSelectbox { margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💖 예서의 무한 변신 옷장 👗")

# --- 이미지 합성 및 크기 자동 조절 함수 ---
def apply_layer(base_img, path, is_hair=False):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            
            # 헤어(Hair)일 경우 특수 크기 조정: 가로를 맞추고 비율 유지
            if is_hair:
                base_w, base_h = base_img.size
                layer_w, layer_h = layer.size
                # 가로 너비를 몸체에 맞춤
                w_ratio = base_w / float(layer_w)
                new_h = int(float(layer_h) * float(w_ratio))
                layer = layer.resize((base_w, new_h), Image.Resampling.LANCZOS)
            else:
                # 일반 의상 및 악세사리는 몸체 크기에 1:1 대응
                layer = layer.resize(base_img.size, Image.Resampling.LANCZOS)
            
            # 합성 (0,0 좌표 기준)
            base_img.alpha_composite(layer, (0, 0))
    except Exception as e:
        pass
    return base_img

# --- 파일 목록 자동 인식 함수 ---
def get_item_list(category):
    items = []
    if os.path.exists(f"{category}.png"): items.append(category)
    for i in range(1, 6): # 1~5번까지 확인
        if os.path.exists(f"{category}{i}.png"): items.append(f"{category}{i}")
    return ["안 함"] + items

# --- 스타일링 메뉴 (탭 구성) ---
tabs = st.tabs(["🏠 배경", "💇 헤어/얼굴", "👗 의상", "🎀 장식"])

with tabs[0]:
    bg_choice = st.selectbox("장소를 선택해요", ["기본 배경", "핑크 방", "푸른 공원"])

with tabs[1]:
    c1, c2 = st.columns(2)
    with c1: hair_choice = st.selectbox("헤어 스타일", get_item_list("헤어"))
    with c2: eye_choice = st.selectbox("예쁜 눈", get_item_list("눈"))
    mouth_choice = st.selectbox("입 모양", get_item_list("입"))

with tabs[2]:
    style_type = st.radio("의상 종류", ["한벌 옷", "상의 & 하의"], horizontal=True)
    if style_type == "한벌 옷":
        onepiece_choice = st.selectbox("원피스", get_item_list("한벌"))
        top_choice, bottom_choice = "안 함", "안 함"
    else:
        c1, c2 = st.columns(2)
        with c1: top_choice = st.selectbox("상의", get_item_list("상의"))
        with c2: bottom_choice = st.selectbox("하의", get_item_list("하의"))
        onepiece_choice = "안 함"

with tabs[3]:
    c1, c2 = st.columns(2)
    with c1: hat_choice = st.selectbox("모자", get_item_list("모자"))
    with c2: acc_choice = st.selectbox("액세서리", get_item_list("악세사리"))

# --- 메인 캔버스 생성 및 합성 ---
try:
    # 1. 배경 (800x1200 세로 비율 고정)
    bg_file = "bg1.png" if bg_choice == "핑크 방" else "bg2.png" if bg_choice == "푸른 공원" else None
    if bg_file and os.path.exists(bg_file):
        canvas = Image.open(bg_file).convert("RGBA").resize((800, 1200))
    else:
        canvas = Image.new("RGBA", (800, 1200), (255, 245, 250, 255))

    # 2. 캐릭터 몸체
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 3. 레이어 합성 순서 (얼굴 -> 헤어 -> 옷 -> 소품)
        if eye_choice != "안 함": canvas = apply_layer(canvas, f"{eye_choice}.png")
        if mouth_choice != "안 함": canvas = apply_layer(canvas, f"{mouth_choice}.png")
        if hair_choice != "안 함": canvas = apply_layer(canvas, f"{hair_choice}.png", is_hair=True)
        
        if style_type == "한벌 옷":
            if onepiece_choice != "안 함": canvas = apply_layer(canvas, f"{onepiece_choice}.png")
        else:
            if top_choice != "안 함": canvas = apply_layer(canvas, f"{top_choice}.png")
            if bottom_choice != "안 함": canvas = apply_layer(canvas, f"{bottom_choice}.png")
            
        if hat_choice != "안 함": canvas = apply_layer(canvas, f"{hat_choice}.png")
        if acc_choice != "안 함": canvas = apply_layer(canvas, f"{acc_choice}.png")

        st.image(canvas, use_container_width=True)
    else:
        st.error("아빠! 'body.png' 파일이 깃허브에 없는 것 같아요.")

except Exception as e:
    st.info("파일 이름을 확인하고 이미지를 올려주세요! (예: 헤어1.png, 상의2.png 등)")

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
if not any(st.session_state.balloons):
    if st.button("🔄 풍선 다시 불기"):
        st.session_state.balloons = [True] * 5
        st.rerun()
