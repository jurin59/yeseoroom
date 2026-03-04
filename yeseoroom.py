import streamlit as st
from PIL import Image
import os

# 1. 버전 및 페이지 설정
VERSION = "v1.7 (아빠의 좌표 저장 완료)"
st.set_page_config(page_title=f"예서의 마법 옷장 {VERSION}", layout="centered")

st.markdown(f"<div style='text-align:right; color:pink; font-weight:bold;'>최종 완성 버전: {VERSION}</div>", unsafe_allow_html=True)
st.title("💖 예서의 무한 변신 옷장 👗")

# --- 💾 [아빠가 찾으신 마법의 숫자들] ---
# 알려주신 좌표를 그대로 입력했습니다. 상하의는 모든 번호에 공통 적용됩니다.
PART_CONFIG = {
    "기본": {"x": 0, "y": 0, "s": 1.0},
    "헤어1": {"x": 0, "y": -82, "s": 0.72},
    "헤어2": {"x": 25, "y": -93, "s": 0.82},
    "상의_공통": {"x": 25, "y": 51, "s": 1.14},
    "하의_공통": {"x": 25, "y": 270, "s": 1.3}
}

# --- 이미지 합성 함수 ---
def apply_layer(base_img, path, item_name):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            
            # 1. 설정값 불러오기
            if "헤어1" in item_name: cfg = PART_CONFIG["헤어1"]
            elif "헤어2" in item_name: cfg = PART_CONFIG["헤어2"]
            elif "상의" in item_name: cfg = PART_CONFIG["상의_공통"]
            elif "하의" in item_name: cfg = PART_CONFIG["하의_공통"]
            else: cfg = PART_CONFIG["기본"]
            
            # 2. 크기 조절
            bg_w, bg_h = base_img.size
            new_w = int(bg_w * cfg["s"])
            new_h = int(layer.size[1] * (new_w / layer.size[0]))
            layer = layer.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # 3. 위치 합성 (가로 중앙 기준 + 오프셋)
            start_x = (bg_w - new_w) // 2 + cfg["x"]
            base_img.alpha_composite(layer, (start_x, cfg["y"]))
    except:
        pass
    return base_img

# --- 파일 목록 가져오기 ---
def get_list(cat):
    items = ["안 함"]
    if os.path.exists(f"{cat}.png"): items.append(cat)
    for i in range(1, 10):
        if os.path.exists(f"{cat}{i}.png"): items.append(f"{cat}{i}")
    return items

# --- 🎮 코디 메뉴 (눈 메뉴는 삭제됨) ---
st.subheader("🎨 예서가 직접 골라보세요!")
c1, c2 = st.columns(2)
with c1:
    hair_choice = st.selectbox("💇 예쁜 머리", get_list("헤어"))
    mouth_choice = st.selectbox("👄 입 모양", get_list("입"))
with c2:
    top_choice = st.selectbox("👕 상의", get_list("상의"))
    bottom_choice = st.selectbox("👖 하의", get_list("하의"))

# --- 캐릭터 출력 영역 ---
try:
    # 배경 생성
    canvas = Image.new("RGBA", (800, 1200), (255, 245, 250, 255))
    
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 1. 입 모양
        if mouth_choice != "안 함":
            canvas = apply_layer(canvas, f"{mouth_choice}.png", mouth_choice)
        
        # 2. 헤어 (아빠가 맞춘 좌표 적용)
        if hair_choice != "안 함":
            canvas = apply_layer(canvas, f"{hair_choice}.png", hair_choice)
            
        # 3. 상의 (공통 좌표 적용)
        if top_choice != "안 함":
            canvas = apply_layer(canvas, f"{top_choice}.png", top_choice)
            
        # 4. 하의 (공통 좌표 적용)
        if bottom_choice != "안 함":
            canvas = apply_layer(canvas, f"{bottom_choice}.png", bottom_choice)

        st.image(canvas, use_container_width=True)
    else:
        st.error("아빠! 깃허브에 'body.png'가 없으면 캐릭터가 안 보여요!")
except:
    st.write("마법으로 옷 입히는 중... ✨")

# --- 🎈 풍선 파티 ---
st.divider()
if st.button("🎈 풍선 팡팡 터뜨리기"):
    st.balloons()
    st.success("예서야, 아빠가 만든 옷장이 마음에 드니? 🎉")
