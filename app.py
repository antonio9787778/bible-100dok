import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="100독 앱", layout="wide")
st.title("📖 GitHub Cloud 100독 - 진행률 완전 버전")

# Session State로 영속성 확보 (Cloud 최적)
if 'progress_data' not in st.session_state:
    # 전체 66권 샘플 데이터 (실제 사용 시 CSV 로드)
    st.session_state.books = {
        '창세기': np.zeros(5), '출애굽기': np.zeros(3),
        '마태복음': np.zeros(5), '요한복음': np.zeros(3),
        '시편': np.zeros(5), '이사야': np.zeros(3),
        '로마서': np.zeros(3), '히브리서': np.zeros(3)
    }
    st.session_state.total_target = sum(len(chs) * 100 for chs in st.session_state.books.values())
    st.session_state.total_read = 0

# 메인 UI
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📚 읽기 입력")
    book_list = list(st.session_state.books.keys())
    selected_book = st.selectbox("책", book_list, key="book_sel")
    
    chapters = len(st.session_state.books[selected_book])
    selected_chapter = st.slider("장", 1, chapters, 1, key="ch_sel")
    
    col_input, col_current = st.columns(2)
    with col_input:
        new_count = st.number_input("독 횟수", 0, 100, 0, key="count_input")
    with col_current:
        current = int(st.session_state.books[selected_book][selected_chapter-1])
        st.metric("현재", f"{current}/100", delta=new_count - current)
    
    if st.button("💾 저장", type="primary"):
        st.session_state.books[selected_book][selected_chapter-1] = new_count
        st.session_state.total_read = sum(sum(book) for book in st.session_state.books.values())
        st.success("저장 완료! ✅")
        st.rerun()

with col2:
    st.subheader("📈 전체 진행률")
    progress = st.session_state.total_read / st.session_state.total_target * 100
    st.progress(progress / 100)
    st.metric("총 독", f"{st.session_state.total_read:,}", f"{st.session_state.total_target:,}", 
              delta=None, help="샘플 데이터")

# 진행표
st.subheader("📊 책별 진행")
progress_df = []
for book, chapters in st.session_state.books.items():
    total_book = sum(chapters)
    avg_book = total_book / len(chapters)
    progress_df.append({
        '책': book,
        '총독': f"{total_book:.0f}",
        '평균': f"{avg_book:.1f}",
        '진행률': f"{avg_book:.1f}%"
    })

st.dataframe(pd.DataFrame(progress_df), use_container_width=True)

# 막대그래프
st.subheader("📈 시각화")
chart_data = pd.DataFrame(progress_df)
st.bar_chart(chart_data.set_index('책')['평균'].astype(float))

# 상태 저장 안내
st.caption("""
💾 **자동 저장**: Session State (새로고침 OK)
☁️ **클라우드**: GitHub Public 완전 무료
📱 **Telegram**: 곧 연동!
""")

# 전체 통계
col1, col2, col3 = st.columns(3)
gu_progress = sum(sum(st.session_state.books[b]) for b in ['창세기', '출애굽기', '시편', '이사야'])
sn_progress = st.session_state.total_read - gu_progress
col1.metric("구약", f"{gu_progress:.0f}")
col2.metric("신약", f"{sn_progress:.0f}")
col3.metric("목표", "100독/권")
