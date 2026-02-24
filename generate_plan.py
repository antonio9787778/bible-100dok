import pandas as pd

# 66권 정확한 장 수
chapter_counts = {
    '창세기':50, '출애굽기':40, '레위기':27, '민수기':36, '신명기':34,
    '여호수아':24, '사사기':21, '룻기':4, '사무엘상':31, '사무엘하':24,
    '열왕기상':22, '열왕기하':25, '역대상':29, '역대하':36, '에스라':10,
    '느헤미야':13, '에스더':10, '욥기':42, '시편':150, '잠언':31,
    '전도서':12, '아가':8, '이사야':66, '예레미야':52, '예레미야애가':5,
    '에스겔':48, '다니엘':12, '호세아':14, '요엘':3, '아모스':9,
    '오바댜':1, '요나':4, '미가':7, '나훔':3, '하박국':3,
    '스바냐':3, '학개':2, '스가랴':14, '말라기':4,
    '마태복음':28, '마가복음':16, '누가복음':24, '요한복음':21,
    '사도행전':28, '로마서':16, '고린도전서':16, '고린도후서':13,
    '갈라디아서':6, '에베소서':6, '빌립보서':4, '골로새서':4,
    '데살로니가전서':5, '데살로니가후서':3, '디모데전서':6, '디모데후서':4,
    '디도서':3, '빌레몬서':1, '히브리서':13, '야고보서':5,
    '베드로전서':5, '베드로후서':3, '요한일서':5, '요한이서':1, 
    '요한삼서':1, '유다서':1, '요한계시록':22
}

# 수정: list로 변환 후 슬라이싱
books = list(chapter_counts.keys())
gu_books = books[:39]  # 구약 39권
sn_books = books[39:]  # 신약 27권

data = []
for book in gu_books:
    for ch in range(1, chapter_counts[book] + 1):
        data.append({'testament': '구약', 'book': book, 'chapter': ch, 'read_count': 0})

for book in sn_books:
    for ch in range(1, chapter_counts[book] + 1):
        data.append({'testament': '신약', 'book': book, 'chapter': ch, 'read_count': 0})

df = pd.DataFrame(data)
df.to_csv('bible_100plan.csv', index=False, encoding='utf-8-sig')
print("✅ bible_100plan.csv 생성 완료! (총 1,189장)")
print(f"구약: {len([x for x in data if x['testament']=='구약'])}장")
print(f"신약: {len(data) - len([x for x in data if x['testament']=='구약'])}장")
print("\n앱 실행: streamlit run bible_100_final.py")
