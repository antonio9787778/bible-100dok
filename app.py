import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="100독 앱", layout="wide")
st.title("📖 Cloud 100독 - 진행률 완전 버전")

# Session State 초기화
if 'books' not in st.session_state:
    st.session_state.books = {
        '창세기': np.zeros(5), '출애굽기': np.zeros(3), '시편': np.zeros(5),
        '마태복음': np.zeros(5), '요한복음': np.zeros(3), '로마서': np.zeros(3)
    }
    st.session_state.total_target = sum(len(v) * 100 for v in st.session_state.books.values())

# 메인 입력
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📚 오늘 읽기")
    book_list = list(st.session_state.books.keys())
    book = st.selectbox("책", book_list)
    chapters = len(st.session_state.books[book])
    chapter = st.slider("장", 1, chapters, 1)
    
    current = int(st.session_state.books[book][chapter-1])
    new_count = st.number_input("독 횟수 (0-100)", 0, 100, current)
    
    if st.button("💾 저장", type="primary"):
        st.session_state.books[book][chapter-1] = new_count
        st.rerun()
    
    st.metric("이번 장", f"{current}/100")

with col2:
    st.subheader("📈 전체 진행")
    total_read = sum(sum(book_chs) for book_chs in st.session_state.books.values())
    progress_pct = total_read / st.session_state.total_target * 100
    st.progress(progress_pct / 100)
    st.metric("총 독", f"{int(total_read)}", f"{int(st.session_state.total_target)}")

# 책별 진행표
st.subheader("📊 책별 진행")
progress_data = []
for book, chapters in st.session_state.books.items():
    book_total = sum(chapters)
    book_avg = book_total / len(chapters)
    progress_data.append({
        '책': book,
        '독': f"{book_total:.0f}",
        '평균': f"{book_avg:.1f}"
    })
st.dataframe(pd.DataFrame(progress_data), use_container_width=True)

# 그래프
st.subheader("📈 진행률 그래프")
chart_df = pd.DataFrame(progress_data)
st.bar_chart(chart_df.set_index('책')['평균'].astype(float))

# 구약/신약 분리
gu_books = ['창세기', '출애굽기', '시편']
sn_books = [b for b in st.session_state.books if b not in gu_books]
gu_total = sum(sum(st.session_state.books[b]) for b in gu_books)
sn_total = sum(sum(st.session_state.books[b]) for b in sn_books)

col1, col2 = st.columns(2)
col1.metric("구약", f"{int(gu_total)}독")
col2.metric("신약", f"{int(sn_total)}독")

st.caption("✅ Cloud 완전 버전 | 새로고침 안전 | 개인 Session State")
