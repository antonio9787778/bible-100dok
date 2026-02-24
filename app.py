import streamlit as st
import pandas as pd
import os

st.title("☁️ GitHub 100독 웹앱")

@st.cache_data
def load_data():
    return pd.read_csv('bible_plan.csv')

df = load_data()

# GitHub 저장 (API 또는 파일)
def save_to_github(count_dict):
    # GitHub API 또는 파일 방식 (간단히 CSV overwrite)
    df['read_count'] = df['read_count'].fillna(0)
    df.to_csv('bible_plan.csv', index=False)

# UI (간소화)
book = st.selectbox("책", df['book'].unique())
chapter = st.selectbox("장", df[df['book']==book]['chapter'])
current = df[(df['book']==book) & (df['chapter']==chapter)]['read_count'].iloc[0]
new_count = st.number_input("독 수", 0, 100, int(current))

if st.button("저장"):
    idx = df[(df['book']==book) & (df['chapter']==chapter)].index[0]
    df.at[idx, 'read_count'] = new_count
    df.to_csv('bible_plan.csv', index=False)
    st.success("GitHub 저장 완료!")

st.metric("총 진행", f"{df['read_count'].sum()}/118900")
