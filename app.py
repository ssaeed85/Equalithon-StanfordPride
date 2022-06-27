import pandas as pd
import numpy as np
import streamlit as st
np.random.seed(42)

st.title("Stanford Pride Member Reconciliation")

df_mc = None

file_saa = st.file_uploader("Select the Stanford Alumni Database Excel export", type="xlsx")
if file_saa is not None:
    df_saa = pd.read_excel(file_saa)

    
file_mc = st.file_uploader("Select the Mail Chimp cleaned list export", type="csv")
if file_mc is not None:
    df_mc = pd.read_csv(file_mc)
if df_mc is not None:    
    st.table(df_mc[['First Name','Last Name','Chapter', 'Degree','Email Address']])





with st.sidebar:
    st.header('Get Possible matches')
    if df_mc is not None:
        rec_num = st.number_input('Select record to match:',min_value=0,max_value=df_mc.shape[0],value=0)
        run_query = st.button('Get Results')



        
if run_query:
    st.write('Getting results: (Hardcoded to return top 5 SAA records)')
    
    st.table(df_saa.head())
    
    