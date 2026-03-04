import streamlit as st
from PIL import Image
import os

# 1. 버전 표시 (업데이트 확인용)
VERSION = "v1.6 (단일 화면 조절판)"
st.set_page_config(page_title=f"예서의 마법 옷장 {VERSION}", layout="centered")

st.markdown(f"<div style='text-align:right; color:gray;'>최종 버전: {VERSION}</div>", unsafe_allow_html=True)
st.title("💖 예서의 무한 조절 옷장 👗")

# --- 💡 [아빠의 저장 장부] ---
# 조절기에서 찾은 숫자를 여기에 적으면 영구 저장됩니다!
PART_CONFIG = {
    "기본": {"x": 0, "y": 0, "s": 1.0},
    "헤어1": {"x": 0, "y": -30, "s": 1.05}, # 예시: 숫자를 여기서 바꾸면 저장돼요!
}

# --- 이미지 합성 함수 ---
def apply_layer(base_img, path, x, y, s):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            bg_w, bg_h = base_img.size
            new_w = int(bg_w * s)
            new_h = int(layer.size[1] * (new_w / layer.size[0]))
            layer = layer.resize((new_w, new_h), Image.Resampling.LANCZOS)
            start_x = (bg_w - new_w) // 2 + x
            base_img.alpha_composite(layer, (start_x, y))
    except:
        pass
    return base_img

# --- 파일 목록 가져오기 ---
def get_list(cat):
    items = ["안 함"]
    if os.path.exists(f"{cat}.png"): items.append(cat)
    for i in range(1, 10): # 9번까지 넉넉하게 확인
        if os.path.exists(f"{cat}{i}.png"): items.append(f"{cat}{i}")
    return items

# --- 🛠️ 조절 도구 (화면 상단에 고정) ---
with st.expander("🛠️ 마법 조절기 열기 (여기서 위치를 맞춰보세요)", expanded=True):
    st.write("아이템을 선택한 후 아래 바를 움직이세요!")
    adj_x = st.sidebar.slider("가로(X)", -400, 400, 0) # 모바일이면 사이드바에, PC면 옆에 나와요
    adj_y = st.slider("세로(Y)", -400, 800, 0)
    adj_s = st.slider("크기(Scale)", 0.5, 2.0, 1.0, 0.01)
    
    # 아빠가 찾으시는 숫자! 크게 보여드립니다.
    st.success(f"📍 이 숫자를 메모하세요 -> x: {adj_x},  y: {adj_y},  s: {adj_s}")

# --- 🎮 아이템 선택 영역 ---
c1, c2 = st.columns(2)
with c1:
    hair = st.selectbox("💇 헤어", get_list("헤어"))
    eye = st.selectbox("👀 눈", get_list("눈"))
with c2:
    top = st.selectbox("👕 상의", get_list("상의"))
    bottom = st.selectbox("👖 하의", get_list("하의"))

# --- 실시간 캐릭터 출력 ---
try:
    canvas = Image.new("RGBA", (800, 1200), (255, 245, 250, 255))
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 선택된 것들 그리기
        items_to_draw = [("눈", eye), ("헤어", hair), ("상의", top), ("하의", bottom)]
        
        for cat, name in items_to_draw:
            if name != "안 함":
                img_path = f"{name}.png"
                # [중요] 지금 조절 중인 값(adj_x, adj_y, adj_s)을 모든 아이템에 실시간 적용!
                canvas = apply_layer(canvas, img_path, adj_x, adj_y, adj_s)

        st.image(canvas, use_container_width=True)
except:
    st.write("이미지를 불러오는 중입니다... ✨")

# --- 풍선 파티 ---
st.divider()
if st.button("🎈 축하 풍선 터뜨리기"):
    st.balloons()
