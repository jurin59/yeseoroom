import streamlit as st
from PIL import Image
import os

# 1. 모바일 우선 설정
st.set_page_config(
    page_title="예서의 마법 옷장",
    layout="centered", # 모바일은 중앙 집중형이 보기 편해요
    initial_sidebar_state="collapsed" # 사이드바를 일단 접어서 화면을 넓게 써요
)

# 모바일에서 글자가 잘 보이도록 CSS 스타일 추가
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; height: 3em; font-size: 1.2rem !important; }
    .stCheckbox { font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("💖 예서의 모바일 옷장 👗")

# --- 이미지 합성 함수 ---
def apply_layer(base_img, path):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            base_img.alpha_composite(layer.resize(base_img.size))
    except:
        pass
    return base_img

# --- 상단 조작 영역 (모바일은 위에서 아래로 흐르는 게 편함) ---
st.subheader("🎨 어떻게 꾸밀까요?")
tab1, tab2, tab3 = st.tabs(["🏠 배경", "👗 의상", "🎀 장식"])

with tab1:
    bg_choice = st.selectbox("장소를 골라요", ["기본 배경", "핑크 방", "푸른 공원"], key="bg")

with tab2:
    outfit_choice = st.radio("오늘의 옷", ["입기 전", "첫 번째 스타일", "두 번째 스타일"], horizontal=True)

with tab3:
    st.write("액세서리를 골라보세요!")
    col_a, col_b = st.columns(2)
    with col_a:
        acc1 = st.checkbox("토끼 키링 🐰")
        acc2 = st.checkbox("반짝 목걸이 ✨")
    with col_b:
        acc3 = st.checkbox("예쁜 가방 👜")
        acc4 = st.checkbox("리본 머리띠 🎀")

# --- 메인 화면 그리기 ---
st.divider()

try:
    # 1. 배경 설정 (800x1200 세로 비율)
    bg_file = "bg1.png" if bg_choice == "핑크 방" else "bg2.png" if bg_choice == "푸른 공원" else None
    if bg_file and os.path.exists(bg_file):
        canvas = Image.open(bg_file).convert("RGBA").resize((800, 1200))
    else:
        canvas = Image.new("RGBA", (800, 1200), (255, 245, 250, 255))

    # 2. 캐릭터 몸체 (body.png)
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)
        
        # 3. 의상 입히기
        if outfit_choice == "첫 번째 스타일":
            canvas = apply_layer(canvas, "outfit1.png")
        elif outfit_choice == "두 번째 스타일":
            canvas = apply_layer(canvas, "outfit2.png")
            
        # 4. 액세서리 입히기
        if acc1: canvas = apply_layer(canvas, "acc1.png")
        if acc2: canvas = apply_layer(canvas, "acc2.png")
        if acc3: canvas = apply_layer(canvas, "acc3.png")
        if acc4: canvas = apply_layer(canvas, "acc4.png")

        # 5. 최종 결과물 출력 (모바일 너비에 맞
