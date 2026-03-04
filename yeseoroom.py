import streamlit as st
from PIL import Image
import os

# 1. 버전 및 페이지 설정
VERSION = "v1.5 (실시간 조절기 탑재)"
st.set_page_config(page_title=f"예서의 마법 옷장 {VERSION}", layout="centered")

st.title("💖 예서의 무한 조절 옷장 👗")
st.write(f"현재 버전: {VERSION}")

# --- 💡 [아빠의 저장 장부] ---
# 조절기에서 찾은 숫자를 여기에 '파츠이름': {x, y, s} 형식으로 적으면 저장됩니다!
PART_CONFIG = {
    "기본": {"x": 0, "y": 0, "s": 1.0},
    "헤어1": {"x": 0, "y": -20, "s": 1.0}, # 예시 수치
}

# --- 이미지 합성 함수 ---
def apply_layer(base_img, path, x, y, s):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            bg_w, bg_h = base_img.size
            # 크기 조절
            new_w = int(bg_w * s)
            new_h = int(layer.size[1] * (new_w / layer.size[0]))
            layer = layer.resize((new_w, new_h), Image.Resampling.LANCZOS)
            # 위치 합성 (중앙 기준 + 오프셋)
            start_x = (bg_w - new_w) // 2 + x
            base_img.alpha_composite(layer, (start_x, y))
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

# --- 메뉴 구성 ---
tabs = st.tabs(["🎮 게임하기", "🛠️ 마법 조절기"])

with tabs[1]:
    st.warning("⚠️ 여기서 조절한 숫자를 메모해서 코드의 PART_CONFIG에 적어주세요!")
    adj_x = st.slider("가로 위치 (X)", -400, 400, 0, key="slider_x")
    adj_y = st.slider("세로 위치 (Y)", -400, 800, 0, key="slider_y")
    adj_s = st.slider("크기 비율 (S)", 0.5, 2.0, 1.0, 0.01, key="slider_s")
    
    # 아빠가 찾으시는 '숫자 확인' 위치!
    st.success(f"📍 메모할 숫자 -> x: {adj_x},  y: {adj_y},  s: {adj_s}")

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        hair = st.selectbox("💇 헤어 선택", get_list("헤어"))
        eye = st.selectbox("👀 눈 선택", get_list("눈"))
    with c2:
        top = st.selectbox("👕 상의 선택", get_list("상의"))
        bottom = st.selectbox("👖 하의 선택", get_list("하의"))

# --- 실시간 렌더링 영역 ---
try:
    canvas = Image.new("RGBA", (800, 1200), (255, 245, 250, 255))
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 선택된 파츠 리스트
        selected_items = [("눈", eye), ("헤어", hair), ("상의", top), ("하의", bottom)]

        for cat, name in selected_items:
            if name != "안 함":
                img_path = f"{name}.png"
                # 만약 '마법 조절기' 탭을 보고 있다면 슬라이더 값을 즉시 적용!
                if st.session_state.get('active_tab') == "🛠️ 마법 조절기": # 탭 인식 로직 (간소화)
                    canvas = apply_layer(canvas, img_path, adj_x, adj_y, adj_s)
                else:
                    # 평소에는 PART_CONFIG에 저장된 값을 사용
                    cfg = PART_CONFIG.get(name, {"x": 0, "y": 0, "s": 1.0})
                    canvas = apply_layer(canvas, img_path, cfg["x"], cfg["y"], cfg["s"])

        st.image(canvas, use_container_width=True)
except Exception as e:
    st.write("이미지를 불러오는 중입니다... 잠시만 기다려주세요! ✨")
