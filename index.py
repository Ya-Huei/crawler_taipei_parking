import streamlit as st
import pandas as pd
from crawler import startCrawler

search_data = st.text_area('車牌數據：', max_chars=65535, height=120,
                           placeholder='以逗號和跳行做分隔\n例如：\nABC-1234,機車\nDEF-5678,汽車')
submit = st.button('查詢')
st.markdown("""---""")

if submit:
    search_data_array = search_data.split('\n')

    result = startCrawler(search_data_array)

    st.text('查詢結果:')
    df = pd.DataFrame(
        result,
        columns=('車牌', '車種', '單號', '停車日期', '時間', '繳費期限'))

    st.dataframe(df)
