import streamlit as st
from PIL import Image
import os

# 1. 버전 및 페이지 설정
VERSION = "v1.3 (조절 도구 포함)"
st.set_page_config(page_title=f"예서의 마법 옷장 {VERSION}", layout="centered")

st.markdown(f"""
    <style>
    .stButton>button {{ width: 100%; border-radius: 12px; height: 3.5em; background-color: #FFB6C1; color: white; }}
    .info-box {{ background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #dcdfe6; }}
    </style>
    <div style="text-align:right; color:gray;">{VERSION}</div>
    """, unsafe_allow_html=True)

st.title("💖 예서의 무한 조절 옷장 👗")

# --- 이미지 합성 함수 (위치/크기 정밀 조절) ---
def apply_layer(base_img, path, x_off=0, y_off=0, scale=1.0):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            # 1. 크기 조절
            bg_w, bg_h = base_img.size
            new_w = int(bg_w * scale)
            new_h = int(layer.size[1] * (new_w / layer.size[0]))
            layer = layer.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # 2. 합성 (중앙 기준 + 오프셋)
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

# --- 메뉴 구성 (조절 도구 탭 추가) ---
tabs = st.tabs(["🎮 옷 입히기", "🛠️ 마법 조절 도구", "🏠 배경 선택"])

with tabs[1]:
    st.markdown("<div class='info-box'><b>🔧 조절 가이드</b><br>1. 왼쪽에서 아이템을 고르세요.<br>2. 아래 바를 움직여 위치를 맞추세요.<br>3. 예쁘게 맞춘 뒤 아래 숫자를 기억하세요!</div>", unsafe_allow_html=True)
    edit_on = st.toggle("조절 모드 켜기")
    if edit_on:
        adj_x = st.slider("가로 이동 (좌/우)", -400, 400, 0)
        adj_y = st.slider("세로 이동 (상/하)", -400, 800, 0)
        adj_s = st.slider("크기 조절", 0.1, 2.5, 1.0, 0.05)
    else:
        adj_x, adj_y, adj_s = 0, 0, 1.0

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        hair_choice = st.selectbox("💇 헤어", get_list("헤어"))
        eye_choice = st.selectbox("👀 눈", get_list("눈"))
    with col2:
        top_choice = st.selectbox("👕 상의", get_list("상의"))
        bottom_choice = st.selectbox("👖 하의", get_list("하의"))
    one_choice = st.selectbox("👗 한벌 옷", get_list("한벌"))
    hat_choice = st.selectbox("👒 모자/장식", get_list("모자"))

with tabs[2]:
    bg_list = ["기본"] + [f"배경{i}" for i in range(1, 6) if os.path.exists(f"배경{i}.png")]
    bg_choice = st.selectbox("배경 선택", bg_list)

# --- 메인 그리기 ---
try:
    if bg_choice != "기본" and os.path.exists(f"{bg_choice}.png"):
        canvas = Image.open(f"{bg_choice}.png").convert("RGBA").resize((800, 1200))
    else:
        canvas = Image.new("RGBA", (800, 1200), (255, 245, 250, 255))

    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # [아빠가 고쳐야 할 부분] 예: hair1의 위치를 잡았다면 여기에 (x, y, scale)을 입력하세요.
        # 예: if hair_choice == "헤어1": canvas = apply_layer(canvas, "헤어1.png", 0, -50, 1.1)
        
        # 현재 조절바 값이 적용되는 로직 (조절 모드 켰을 때만 작동)
        if edit_on:
            # 마지막으로 선택한 것이 무엇이든 조절바 값이 적용되어 보여줍니다.
            if eye_choice != "안 함": canvas = apply_layer(canvas, f"{eye_choice}.png", adj_x, adj_y, adj_s)
            if hair_choice != "안 함": canvas = apply_layer(canvas, f"{hair_choice}.png", adj_x, adj_y, adj_s)
            if top_choice != "안 함": canvas = apply_layer(canvas, f"{top_choice}.png", adj_x, adj_y, adj_s)
            # ... 필요한 만큼 추가 가능
        else:
            # 평소 모드 (기본 위치)
            if eye_choice != "안 함": canvas = apply_layer(canvas, f"{eye_choice}.png", 0, 0, 1.0)
            if hair_choice != "안 함": canvas = apply_layer(canvas, f"{hair_choice}.png", 0, -20, 1.0) # 기본 헤어 위치 보정
            if top_choice != "안 함": canvas = apply_layer(canvas, f"{top_choice}.png", 0, 150, 1.0)
            if bottom_choice != "안 함": canvas = apply_layer(canvas, f"{bottom_choice}.png", 0, 450, 1.0)
            if one_choice != "안 함": canvas = apply_layer(canvas, f"{one_choice}.png", 0, 150, 1.0)
            if hat_choice != "안 함": canvas = apply_layer(canvas, f"{hat_choice}.png", 0, -50, 1.0)

        st.image(canvas, use_container_width=True)
        
        if edit_on:
            st.success(f"📍 현재 수치 저장용: 가로({adj_x}), 세로({adj_y}), 크기({adj_s})")
    else:
        st.error("body.png 파일이 필요합니다!")
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
                st.balloons()
                st.rerun()
        else: st.write("💥")
