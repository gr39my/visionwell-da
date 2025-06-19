import uuid
import streamlit as st
from urllib.parse import parse_qs
from db import get_conn

st.title('生徒新規登録')

query_params = st.experimental_get_query_params()
token = query_params.get('token', [None])[0]

if not token:
    st.error('招待トークンが見つかりません')
    st.stop()

# validate token
with get_conn() as conn:
    cur = conn.execute('SELECT used FROM invitations WHERE token=?', (token,))
    row = cur.fetchone()
    if not row:
        st.error('無効な招待トークンです')
        st.stop()
    if row[0]:
        st.error('この招待トークンは既に使用されています')
        st.stop()

with st.form('register'):
    email = st.text_input('メールアドレス')
    password = st.text_input('パスワード', type='password')
    birthdate = st.date_input('生年月日')
    current_grade = st.number_input('今の学年', min_value=1, max_value=6, step=1)
    class_year1 = st.text_input('1年次のクラス')
    class_year2 = st.text_input('2年次のクラス')
    class_year3 = st.text_input('3年次のクラス')
    submitted = st.form_submit_button('登録')

    if submitted:
        if not email or not password:
            st.error('メールアドレスとパスワードを入力してください')
        else:
            try:
                with get_conn() as conn:
                    conn.execute(
                        'INSERT INTO users (email, password, birthdate, current_grade, class_year1, class_year2, class_year3) VALUES (?,?,?,?,?,?,?)',
                        (
                            email,
                            password,
                            birthdate.isoformat(),
                            current_grade,
                            class_year1,
                            class_year2,
                            class_year3,
                        ),
                    )
                    conn.execute(
                        'UPDATE invitations SET used=1 WHERE token=?',
                        (token,),
                    )
                    st.success('登録が完了しました')
                    st.stop()
            except Exception as e:
                st.error('登録に失敗しました')

