import streamlit as st
from PIL import Image

# 페이지 설정
st.set_page_config(page_title="예서의 마법 옷장", layout="wide")

st.title("💖 예서의 온라인 드레스업 룸 👗")
st.write("왼쪽 메뉴에서 예서가 입고 싶은 옷을 골라보세요!")

# --- 사이드바: 옷 선택 ---
with st.sidebar:
    st.header("🚪 옷장 열기")
    # 예서가 가지고 있는 옷 리스트에 맞춰서 이름을 정해주세요
    outfit_choice = st.radio("어떤 옷을 입을까요?", ["입기 전", "첫 번째 스타일", "두 번째 스타일"])

# --- 메인 화면: 캐릭터 출력 ---
col1, col2 = st.columns([1, 1])

with col1:
    try:
        # 1. 몸체 베이스 (body.png) - 깃허브에 이 이름으로 파일이 있어야 해요!
        base = Image.open("body.png").convert("RGBA")
        
        # 2. 옷 입히기 로직
        if outfit_choice == "첫 번째 스타일":
            cloth = Image.open("outfit1.png").convert("RGBA")
            base.alpha_composite(cloth.resize(base.size))
        elif outfit_choice == "두 번째 스타일":
            cloth = Image.open("outfit2.png").convert("RGBA")
            base.alpha_composite(cloth.resize(base.size))
            
        st.image(base, width=500, caption="✨ 오늘 예서의 선택!")
        
    except FileNotFoundError:
        st.warning("아직 옷 사진이 올라오지 않았어요. 깃허브에 'body.png', 'outfit1.png' 파일을 올려주세요!")

with col2:
    st.subheader("📝 코디 설명")
    st.write("예서가 직접 그린 예쁜 옷들을 웹사이트에서 바로 입혀볼 수 있어요.")
    if st.button("🎉 축하 파티!"):
        st.balloons()
