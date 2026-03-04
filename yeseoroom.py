import streamlit as st
from PIL import Image
from rembg import remove
import io

# 페이지 설정
st.set_page_config(page_title="예서의 드레스업 스튜디오", layout="wide")

# 배경 제거 함수
def remove_bg(upload_file):
    input_data = upload_file.getvalue()
    output_data = remove(input_data)
    return Image.open(io.BytesIO(output_data)).convert("RGBA")

st.title("👗 예서의 마법 옷장 제작소 💄")
st.write("예서가 그린 그림을 올리면 아빠의 컴퓨터가 배경을 지우고 게임으로 만들어줘!")

# --- 사이드바: 파일 업로드 ---
with st.sidebar:
    st.header("📂 그림 업로드")
    body_file = st.file_uploader("1. 캐릭터 몸체 (body.png)", type=["png", "jpg", "jpeg"])
    outfit_file = st.file_uploader("2. 옷/세트 (outfit.png)", type=["png", "jpg", "jpeg"])
    keyring_file = st.file_uploader("3. 가방/키링 (item.png)", type=["png", "jpg", "jpeg"])
    
    st.divider()
    mode = st.radio("모드 선택", ["👗 코디하기", "💄 메이크업"])
    if mode == "💄 메이크업":
        lip_color = st.color_picker("립스틱 색깔", "#FF4B4B")

# --- 메인 화면: 제작 및 미리보기 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🛠️ 이미지 처리 상태")
    
    # 세션 상태에 처리된 이미지 저장 (속도 향상)
    if body_file and 'processed_body' not in st.session_state:
        with st.spinner('캐릭터 배경 지우는 중...'):
            st.session_state.processed_body = remove_bg(body_file)
    
    if outfit_file and 'processed_outfit' not in st.session_state:
        with st.spinner('옷 배경 지우는 중...'):
            st.session_state.processed_outfit = remove_bg(outfit_file)

    if keyring_file and 'processed_keyring' not in st.session_state:
        with st.spinner('키링 배경 지우는 중...'):
            st.session_state.processed_keyring = remove_bg(keyring_file)

    st.write("✅ 모든 준비가 끝났습니다!")

with col2:
    st.subheader("✨ 최종 게임 화면")
    
    if 'processed_body' in st.session_state:
        # 1. 몸체 가져오기
        canvas = st.session_state.processed_body.copy()
        
        # 2. 옷 입히기 (몸체와 같은 크기로 겹침)
        if 'processed_outfit' in st.session_state:
            outfit_img = st.session_state.processed_outfit.resize(canvas.size)
            canvas.alpha_composite(outfit_img)
            
        # 3. 키링/가방 겹치기
        if 'processed_keyring' in st.session_state:
            keyring_img = st.session_state.processed_keyring.resize(canvas.size)
            canvas.alpha_composite(keyring_img)

        # 화면 출력
        st.image(canvas, use_container_width=True)
        
        if mode == "💄 메이크업":
            st.write(f"👄 입술에 {lip_color}색 포인트를 줬어요!")
    else:
        st.info("왼쪽에서 캐릭터 사진을 먼저 올려주세요!")

# 초기화 버튼
if st.button("새로 만들기 (이미지 초기화)"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()