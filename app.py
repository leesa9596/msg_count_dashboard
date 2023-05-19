import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd


st.title("Darinbot Msg Count App")

conn = st.experimental_connection('mysql', type='sql')

msg_df = conn.query('SELECT * from r_msg_count;', ttl=600)

today_date = datetime.now().strftime("%Y-%m-%d")
today_msg = msg_df[msg_df.createdTime>=today_date]
today_msg = today_msg.sort_values(by='createdTime', ascending=False)

num_darinbot = len(today_msg.masterId.unique())
today_msg_sum = today_msg[:num_darinbot][['masterNickname','numMsg']].set_index('masterNickname')

st.line_chart(today_msg_sum)
    
user_input_date = st.text_input("Enter date : (format : %Y-%m-%d)")



try:
    user_input_date_after = (datetime.strptime(user_input_date, "%Y-%m-%d") + relativedelta(days=1)).strftime("%Y-%m-%d")
    select_date_msg = msg_df[(msg_df.createdTime>=user_input_date) & (msg_df.createdTime<user_input_date_after)]
    if len(select_date_msg)==0:
        st.write('nothing to show on selected date')
    else:
        select_date_msg_sum = pd.DataFrame(select_date_msg.groupby('masterNickname')['numMsg'].sum())
        st.write(select_date_msg_sum[select_date_msg_sum.numMsg==0])

        st.bar_chart(select_date_msg_sum)
except ValueError:
    pass
finally:
    pass