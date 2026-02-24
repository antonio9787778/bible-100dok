import streamlit as st
import pandas as pd
import os

st.title("☁️ GitHub 100독 앱 - 평생 100독")

@st.cache_data
def load_data():
    # 여러 파일명 지원
    for filename in ['bible_100plan.csv', 'bible_plan.csv', 'progress.csv']:
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            if 'read_count' not in df.columns:
                df['read_count'] = 0
            return df
    st.error("❌ CSV 파일 없음! generate_plan.py 실행하세요")
    st.stop()

try:
    df = load_data()
    st.success(f"✅ 데이터 로드: {len(df)}장")
    
    # 사이드바 필터
    col1, col2 = st.columns(2)
    with col1:
        testament = st.selectbox("약전", ["전체", "구약", "신약"])
    with col2:
        book_filter = st.text_input("책 검색")
    
    filtered_df = df.copy()
    if testament == "구약":
        filtered_df = filtered_df[filtered_df['testament'] == '구약']
    elif testament == "신약":
        filtered_df = filtered_df[filtered_df['testament'] == '신약']
    if book_filter:
        filtered_df = filtered_df[filtered_df['book'].str.contains(book_filter)]
    
    st.subheader(f"📖 {len(filtered_df)}장 (총 {df['read_count'].sum():,}/118,900)")
    
    # 각 장 입력 (20개씩 페이징)
    for i in range(0, min(20, len(filtered_df)), 1):
        row = filtered_df.iloc[i]
        with st.expander(f"{row['book']} {row['chapter']}장 ({int(row['read_count'])}/100)"):
            col1, col2 = st.columns(2)
            new_count = col1.number_input("독 횟수", 0, 100, int(row['read_count']), 
                                        key=f"row_{i}_{row['book']}_{row['chapter']}")
            
            orig_idx = df[(df['book'] == row['book']) & (df['chapter'] == row['chapter'])].index[0]
            if new_count != df.at[orig_idx, 'read_count']:
                df.at[orig_idx, 'read_count'] = new_count
                df.to_csv('bible_100plan.csv', index=False)
                st.balloons()
    
    # 통계
    col1, col2, col3 = st.columns(3)
    gu = df[df['testament']=='구약']['read_count'].sum()
    sn = df[df['testament']=='신약']['read_count'].sum()
    col1.metric("구약", f"{gu:,}/92,900")
    col2.metric("신약", f"{sn:,}/26,000")
    col3.metric("총계", f"{gu+sn:,}/118,900")
    
    st.caption("GitHub 자동 저장 | 검색 → 입력 → 자동 저장")

except Exception as e:
    st.error(f"오류: {e}")
    st.info("""
1. repo에 bible_100plan.csv 업로드
2. generate_plan.py 실행 (Actions)
3. app.py 저장 후 Reboot
    """)
