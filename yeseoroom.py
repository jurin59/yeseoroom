import streamlit as st
from PIL import Image

st.set_page_config(page_title="예서의 마법 옷장", layout="wide")
st.title("💖 예서의 초스피드 디자인 룸 👗")

st.info("💡 사이트에서 배경을 지운 PNG 파일을 올려주세요!")

with st.sidebar:
    st.header("📂 사진 올리기")
    body_file = st.file_uploader("1. 캐릭터 본체 (PNG)", type=["png"])
    outfit_file = st.file_uploader("2. 옷/아이템 (PNG)", type=["png"])

col1, col2 = st.columns(2)

if body_file:
    body_img = Image.open(body_file).convert("RGBA")
    with col1:
        st.image(body_img, width=400, caption="예서의 캐릭터")
    
    if outfit_file:
        outfit_img = Image.open(outfit_file).convert("RGBA")
        with col2:
            # 캐릭터 크기에 맞춰 옷 크기 자동 조절
            outfit_resized = outfit_img.resize(body_img.size)
            
            # 두 이미지 겹치기
            combined = Image.alpha_composite(body_img, outfit_resized)
            st.image(combined, width=400, caption="✨ 짜잔! 코디 완성")
