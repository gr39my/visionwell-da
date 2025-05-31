import streamlit as st
import pandas as pd
import numpy as np

# 生徒データのサンプル
students = pd.DataFrame({
    'name': ['田中', '佐藤', '鈴木'],
    'grade': [4.3, 3.8, 4.0],
    'teamwork': [0.9, 0.6, 0.8],
    'preferences': [
        ['A', 'B', 'C', 'D', 'E', 'F'],
        ['B', 'A', 'D', 'C', 'E', 'F'],
        ['C', 'A', 'B', 'D', 'F', 'E']
    ]
})

# 学校データとスコア関数
schools = {
    'A': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.7 + s['teamwork'] * 0.3},
    'B': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.6 + s['teamwork'] * 0.4},
    'C': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.8 + s['teamwork'] * 0.2},
    'D': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.5 + s['teamwork'] * 0.5},
    'E': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.9 + s['teamwork'] * 0.1},
    'F': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.4 + s['teamwork'] * 0.6},
}

# Streamlit UI
st.title("高校推薦枠マッチングシステム（DAアルゴリズム）")

# 表1：学生一覧
st.subheader("学生の情報と希望先")
student_display = students.copy()
student_display['preferences'] = student_display['preferences'].apply(lambda prefs: ' > '.join(prefs))
st.dataframe(student_display.rename(columns={
    'name': '氏名',
    'grade': '評定',
    'teamwork': '協調性',
    'preferences': '希望順'
}), use_container_width=True)

# 表2：学校と評価基準
st.subheader("学校ごとの評価基準")
school_display = pd.DataFrame([
    {
        '学校': k,
        '定員': v['capacity'],
        '評価基準': f"評定×{v['score_func']({'grade':1,'teamwork':0})} + 協調性×{v['score_func']({'grade':0,'teamwork':1})}"
    }
    for k, v in schools.items()
])
st.table(school_display)

# Deferred Acceptance アルゴリズム（簡易）
def rank_students(school_key):
    func = schools[school_key]['score_func']
    return sorted(students.to_dict('records'), key=lambda s: -func(s))

def deferred_acceptance():
    proposals = {s['name']: 0 for _, s in students.iterrows()}
    matches = {school: [] for school in schools}
    while True:
        free_students = [s for s in students.to_dict('records') if proposals[s['name']] < 6 and all(s['name'] not in [m['name'] for m in matches[school]] for school in matches)]
        if not free_students:
            break
        for s in free_students:
            choice = s['preferences'][proposals[s['name']]]
            proposals[s['name']] += 1
            if choice in matches:
                matches[choice].append(s)
            else:
                matches[choice] = [s]
            ranked = rank_students(choice)
            matches[choice] = ranked[:schools[choice]['capacity']]
    return matches

# マッチングボタン
if st.button("マッチング開始"):
    results = deferred_acceptance()
    for school, matched in results.items():
        st.subheader(f"{school} に内定した生徒")
        for s in matched:
            st.write(f" - {s['name']}（評定: {s['grade']}, 協調性: {s['teamwork']}）")
