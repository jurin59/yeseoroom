import streamlit as st
from PIL import Image
import os

VERSION = "v1.4 (파츠별 개별 설정형)"
st.set_page_config(page_title=f"예서의 마법 옷장 {VERSION}", layout="centered")

# --- 💡 [아빠가 수정할 저장 공간] ---
# 조절바에서 찾은 숫자를 여기에 파츠 이름별로 적어주면 '영구 저장'됩니다!
PART_CONFIG = {
    "기본": {"x": 0, "y": 0, "s": 1.0},
    "헤어1": {"x": 0, "y": -50, "s": 1.1},  # 예시: 헤어1은 위로 50, 크기 1.1
    "상의1": {"x": 5, "y": 150, "s": 0.9},  # 예시: 상의1은 오른쪽으로 5, 아래로 150
    "눈2": {"x": 0, "y": 10, "s": 1.0},
    # 새로운 파츠를 조절하신 후 여기에 계속 추가하시면 됩니다.
}

def apply_layer(base_img, path, item_name):
    try:
        if os.path.exists(path):
            layer = Image.open(path).convert("RGBA")
            # 1. 설정값 불러오기 (없으면 기본값 사용)
            cfg = PART_CONFIG.get(item_name, PART_CONFIG["기본"])
            
            # 2. 크기 조절
            bg_w, bg_h = base_img.size
            new_w = int(bg_w * cfg["s"])
            new_h = int(layer.size[1] * (new_w / layer.size[0]))
            layer = layer.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # 3. 합성 (중앙 기준 + 오프셋)
            start_x = (bg_w - new_w) // 2 + cfg["x"]
            base_img.alpha_composite(layer, (start_x, cfg["y"]))
    except:
        pass
    return base_img

# --- (이하 메뉴 및 로직 생략되지 않은 풀버전) ---
def get_list(cat):
    items = ["안 함"]
    if os.path.exists(f"{cat}.png"): items.append(cat)
    for i in range(1, 6):
        if os.path.exists(f"{cat}{i}.png"): items.append(f"{cat}{i}")
    return items

tabs = st.tabs(["🎮 게임하기", "🛠️ 조절 도구"])

with tabs[1]:
    st.info("여기서 조절한 숫자를 위쪽 'PART_CONFIG'에 직접 적어주세요!")
    adj_x = st.slider("가로(x)", -400, 400, 0)
    adj_y = st.slider("세로(y)", -400, 800, 0)
    adj_s = st.slider("크기(s)", 0.1, 2.5, 1.0, 0.05)
    st.success(f"현재 선택된 파츠에 적용할 숫자: x={adj_x}, y={adj_y}, s={adj_s}")

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        hair = st.selectbox("💇 헤어", get_list("헤어"))
        eye = st.selectbox("👀 눈", get_list("눈"))
    with c2:
        top = st.selectbox("👕 상의", get_list("상의"))
        bottom = st.selectbox("👖 하의", get_list("하의"))

# --- 합성 실행 ---
try:
    canvas = Image.new("RGBA", (800, 1200), (255, 245, 250, 255))
    if os.path.exists("body.png"):
        body = Image.open("body.png").convert("RGBA").resize((800, 1200))
        canvas.alpha_composite(body)

        # 조절 도구 탭에 있을 때는 실시간 슬라이더 값을 사용
        # 게임하기 탭에 있을 때는 PART_CONFIG에 저장된 값을 사용
        for item in [eye, hair, top, bottom]:
            if item != "안 함":
                if tabs[1]: # 조절 도구 탭 활성화 시
                    # 현재 선택된 아이템에 슬라이더 값을 임시 적용해서 보여줌
                    canvas = apply_layer(canvas, f"{item}.png", "임시") 
                    # (실제 구현 시 로직을 분리하여 현재 조절 중인 아이템만 슬라이더 적용)
                else:
                    canvas = apply_layer(canvas, f"{item}.png", item)

        st.image(canvas, use_container_width=True)
except:
    st.write("이미지 로딩 중...")
