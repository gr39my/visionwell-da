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
}

# 各学校が生徒をスコアで評価して順位付け
def rank_students(school_key):
    func = schools[school_key]['score_func']
    return sorted(students.to_dict('records'), key=lambda s: -func(s))

# Deferred Acceptance アルゴリズム（簡易）
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
            matches[choice].append(s)
            ranked = rank_students(choice)
            matches[choice] = ranked[:schools[choice]['capacity']]
    return matches

# Streamlit UI
st.title("高校推薦枠マッチングシステム（DAアルゴリズム）")

if st.button("マッチング開始"):
    results = deferred_acceptance()
    for school, matched in results.items():
        st.subheader(f"{school} に内定した生徒")
        for s in matched:
            st.write(f" - {s['name']}（評定: {s['grade']}, 協調性: {s['teamwork']}）")
