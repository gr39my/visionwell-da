import streamlit as st
import pandas as pd
from pathlib import Path

st.title("先生画面: 共有シート一覧")

sheet_dir = Path("shared_sheets")

if not sheet_dir.exists():
    st.info("共有シートがありません")
else:
    files = sorted(sheet_dir.glob("*.md"))
    if files:
        data = []
        for f in files:
            name, date = f.stem.split("_", 1)
            data.append({"氏名": name, "年月日": date, "path": f})
        df = pd.DataFrame(data)
        st.dataframe(df[["氏名", "年月日"]])

        option = st.selectbox("閲覧する共有シートを選択", df.index, format_func=lambda i: f"{df.at[i, '氏名']} ({df.at[i, '年月日']})")
        file_path = df.at[option, "path"]
        st.markdown(file_path.read_text(), unsafe_allow_html=True)
    else:
        st.info("共有シートがありません")

