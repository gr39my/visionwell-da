import streamlit as st
import pandas as pd
import numpy as np

# 初期データ
initial_students = pd.DataFrame({
    'name': ['田中', '佐藤', '鈴木'],
    'grade': [4.3, 3.8, 4.0],
    'teamwork': [0.9, 0.6, 0.8],
    'preferences': [
        ['A', 'B', 'C', 'D', 'E', 'F'],
        ['B', 'A', 'D', 'C', 'E', 'F'],
        ['C', 'A', 'B', 'D', 'F', 'E']
    ]
})

schools = {
    'A': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.7 + s['teamwork'] * 0.3},
    'B': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.6 + s['teamwork'] * 0.4},
    'C': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.8 + s['teamwork'] * 0.2},
    'D': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.5 + s['teamwork'] * 0.5},
    'E': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.9 + s['teamwork'] * 0.1},
    'F': {'capacity': 1, 'score_func': lambda s: s['grade'] * 0.4 + s['teamwork'] * 0.6},
}

# Streamlit タイトル
st.title("高校推薦枠マッチングシステム（DAアルゴリズム）")

# セッション状態の初期化
if 'students' not in st.session_state:
    st.session_state.students = initial_students.copy()

# === CSVアップロード ===
st.subheader("CSVアップロード")
uploaded_file = st.file_uploader("CSVファイルを選択", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if 'preferences' in df.columns:
            df['preferences'] = df['preferences'].apply(
                lambda x: [p.strip() for p in str(x).split(',') if p.strip() in schools]
            )
        else:
            pref_cols = [c for c in df.columns if c.startswith('pref')]
            df['preferences'] = df[pref_cols].apply(
                lambda row: [p for p in row if pd.notna(p) and p in schools], axis=1
            )
        st.session_state.students = df[['name', 'grade', 'teamwork', 'preferences']]
        st.success("CSVから学生データを読み込みました")
    except Exception as e:
        st.error("CSVの読み込みに失敗しました")

# === 生徒追加フォーム ===
st.subheader("生徒の追加")

with st.form("add_student_form"):
    name = st.text_input("氏名")
    grade = st.number_input("評定（例: 4.2）", min_value=0.0, max_value=5.0, step=0.1)
    teamwork = st.number_input("協調性（0.0～1.0）", min_value=0.0, max_value=1.0, step=0.1)
    preferences = st.text_input("希望順（カンマ区切り：例 A,B,C）")

    submitted = st.form_submit_button("生徒を追加")
    if submitted:
        prefs = [p.strip() for p in preferences.split(',') if p.strip() in schools]
        if name and prefs:
            st.session_state.students = pd.concat([
                st.session_state.students,
                pd.DataFrame([{
                    'name': name,
                    'grade': grade,
                    'teamwork': teamwork,
                    'preferences': prefs
                }])
            ], ignore_index=True)
            st.success(f"{name} さんを追加しました！")
        else:
            st.error("氏名と希望順（有効な学校名）を入力してください。")

# === 学生一覧表示 ===
st.subheader("学生の情報と希望先")
student_display = st.session_state.students.copy()
student_display['preferences'] = student_display['preferences'].apply(lambda prefs: ' > '.join(prefs))
st.dataframe(student_display.rename(columns={
    'name': '氏名',
    'grade': '評定',
    'teamwork': '協調性',
    'preferences': '希望順'
}), use_container_width=True)

# === 学校の評価基準表示 ===
st.subheader("学校ごとの評価基準")
school_display = pd.DataFrame([
    {
        '学校': k,
        '定員': v['capacity'],
        '評価基準': f"評定×{v['score_func']({'grade':1,'teamwork':0}):.1f} + 協調性×{v['score_func']({'grade':0,'teamwork':1}):.1f}"
    }
    for k, v in schools.items()
])
st.table(school_display)

# === DAアルゴリズム ===
def rank_students(school_key):
    func = schools[school_key]['score_func']
    return sorted(st.session_state.students.to_dict('records'), key=lambda s: -func(s))

def deferred_acceptance():
    students_list = st.session_state.students.to_dict("records")
    proposals = {s['name']: 0 for s in students_list}
    matches = {school: [] for school in schools}
    matched_students = set()

    while True:
        proposals_this_round = {}
        for s in students_list:
            if s['name'] in matched_students:
                continue
            if proposals[s['name']] >= len(s['preferences']):
                continue
            preferred_school = s['preferences'][proposals[s['name']]]
            proposals[s['name']] += 1
            if preferred_school not in proposals_this_round:
                proposals_this_round[preferred_school] = []
            proposals_this_round[preferred_school].append(s)

        if not proposals_this_round:
            break

        for school_key, applicants in proposals_this_round.items():
            current_matched = matches[school_key]
            total_candidates = current_matched + applicants
            func = schools[school_key]['score_func']
            ranked = sorted(total_candidates, key=lambda s: -func(s))
            accepted = ranked[:schools[school_key]['capacity']]
            rejected = set(s['name'] for s in total_candidates) - set(s['name'] for s in accepted)
            matches[school_key] = accepted
            matched_students.update(s['name'] for s in accepted)
            matched_students -= rejected

    return matches

# === マッチング実行ボタン ===
if st.button("マッチング開始"):
    results = deferred_acceptance()
    for school, matched in results.items():
        st.subheader(f"{school} に内定した生徒")
        for s in matched:
            st.write(f" - {s['name']}（評定: {s['grade']}, 協調性: {s['teamwork']}）")