import streamlit as st
from PIL import Image
import io

# 1. 페이지 설정
st.set_page_config(page_title="예서의 마법 옷장", layout="wide")
st.title("💖 예서의 디자인 스튜디오 🎨")

# 2. 사이드바 - 파일 업로드
with st.sidebar:
    st.header("📂 그림 올리기")
    body_file = st.file_uploader("1. 캐릭터 몸체 사진", type=["png", "jpg", "jpeg"])
    outfit_file = st.file_uploader("2. 옷/아이템 사진", type=["png", "jpg", "jpeg"])
    
    st.divider()
    # 서버 부하를 줄이기 위해 버튼을 눌러야만 배경 제거 실행
    run_ai = st.button("✨ 배경 지우기 마법 실행")

# 3. 메인 화면 로직
col1, col2 = st.columns(2)

def process_img(file, apply_ai):
    img = Image.open(file).convert("RGBA")
    if apply_ai:
        from rembg import remove
        return Image.open(io.BytesIO(remove(file.getvalue()))).convert("RGBA")
    return img

with col1:
    if body_file:
        body_img = process_img(body_file, run_ai)
        st.image(body_img, caption="예서의 캐릭터", use_container_width=True)
        st.session_state['body'] = body_img

with col2:
    if outfit_file:
        outfit_img = process_img(outfit_file, run_ai)
        st.image(outfit_img, caption="선택한 아이템", use_container_width=True)
        st.session_state['outfit'] = outfit_img

# 4. 겹쳐보기 결과
if 'body' in st.session_state and 'outfit' in st.session_state:
    st.divider()
    st.subheader("✨ 최종 코디 결과")
    canvas = st.session_state['body'].copy()
    # 아이템을 캐릭터 크기에 맞춰서 겹침
    outfit_resized = st.session_state['outfit'].resize(canvas.size)
    canvas.alpha_composite(outfit_resized)
    st.image(canvas, width=500)
