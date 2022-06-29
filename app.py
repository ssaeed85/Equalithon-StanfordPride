import pandas as pd
import numpy as np
import streamlit as st
np.random.seed(42)


# def _max_width_():
#     max_width_str = f"max-width: 2000px;"
#     st.markdown(
#         f"""
#     <style>
#     .reportview-container .main .block-container{{
#         {max_width_str}
#     }}
#     </style>    
#     """,
#         unsafe_allow_html=True,
#     )



st.title("Stanford Pride Member Reconciliation")

df_mc = None
df_saa = None
run_query=False

# Load SAA db export
file_saa = st.file_uploader("Select the Stanford Alumni Database Excel export", type="xlsx")
if file_saa is not None:
    df_saa = pd.read_excel(file_saa)

# Load MailChimp's cleaned list 
file_mc = st.file_uploader("Select the Mail Chimp cleaned list export", type="csv")
if file_mc is not None:
    df_mc = pd.read_csv(file_mc)
    df_mc['query'] = df_mc.index.astype(str)+ ' ' + df_mc['First Name'] + ' ' + df_mc['Last Name']

# Display MailChimp list
if df_mc is not None:    
    st.dataframe(data = df_mc[['First Name','Last Name',
                'Chapter', 'Country','Degree','Email Address'
                ]]
                )

# Use streamlit's side bar to set up query tools
# Drop down format MC_record_index + First_Name + Last_Names
with st.sidebar:
    st.header('Query SAA database for user')
    if df_saa is not None:
        if df_mc is not None:
            # rec_num = st.number_input('Select record to match:',min_value=0,max_value=df_mc.shape[0]-1,value=0)
            query = st.selectbox(label = 'User to query for',options = df_mc['query'])
            queried_mc_index = int(query.split()[0])
            
            run_query = st.button('Get Results')

        if run_query:
            st.header('Searching for member in SAA database')
            st.write('First Name:', df_mc.loc[queried_mc_index]['First Name'])
            st.write('Last Name:', df_mc.loc[queried_mc_index]['Last Name'])
            st.write('Degree:', df_mc.loc[queried_mc_index]['Degree'])
            st.write('Email:', df_mc.loc[queried_mc_index]['Email Address'])
        
if run_query and df_saa is not None:
    st.write('Getting results: (Hardcoded to return top 5 SAA records)')

    columns = ['first_name','last_name','short_degree_string',
                'home_phone_number','bus_phone_number',
                'home_email_address', 'bus_email_address', 'email_switch',
                'saa_email_address', 'gsb_email_address', 'other_email_address']
    st.dataframe(df_saa.head().filter(columns))
    