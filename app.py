import pandas as pd
import numpy as np
import streamlit as st
np.random.seed(42)

st.title("Stanford Pride Member Reconciliation")

saa_df = pd.read_excel(st.file_uploader("Select the Stanford Alumni Database Excel export", type="xlsx"))
mc_df = pd.read_csv(st.file_uploader("Select the Mail Chimp cleaned list export", type="csv"))

# def runMatchFunc(mc_rec,)
# def runMatch():



with st.sidebar:
    st.header('Get Possible matches')
    rec_num = st.number_input('Select record to match:',min_value=0,max_value=mc_df.shape[0],value=0)
    run_query = st.button('Get Results')


    if run_query:
        #run function to get list of matching records in order of relevance
        #use rec_num to know which mail chimp record to run matching pass on
        recommend_list = [30] #hardcoded for example

        st.table(saa_df.loc[recommend_list[0]])

st.table(mc_df[['First Name','Last Name','Chapter', 'Degree','Email Address']])

