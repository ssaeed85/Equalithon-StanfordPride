import pandas as pd
import numpy as np
import streamlit as st

from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from src.helper_functions import *
st. set_page_config(layout="wide") 



st.title("Stanford Pride Member Reconciliation")

df_mailchimp_original = None
df_saa_original = None
run_query=False
results_dict = None


# Load SAA db export
file_saa = st.file_uploader("Select the Stanford Alumni Database Excel export", type="xlsx")
if file_saa is not None:
    df_saa_original = pd.read_excel(file_saa)

# Load MailChimp's cleaned list 
file_mc = st.file_uploader("Select the Mail Chimp cleaned list export", type="csv")
if file_mc is not None:
    df_mailchimp_original = pd.read_csv(file_mc)
    df_mailchimp_original['query'] =    df_mailchimp_original.index.astype(str)+ ' ' \
                                        + df_mailchimp_original['First Name'] + ' ' \
                                        + df_mailchimp_original['Last Name']

# Display MailChimp list
if df_mailchimp_original is not None:    
    st.markdown('### MailChimp Clean Records')
    st.dataframe(data = df_mailchimp_original[['First Name','Last Name',
                'Chapter', 'Country','Degree','Email Address'
                ]]
                )

# Use streamlit's side bar to set up query tools
# Drop down format MC_record_index + First_Name + Last_Names
with st.sidebar:
    st.header('Query SAA database for user')
    if df_saa_original is not None:
        #Only show query controls if both files are loaded
        if df_mailchimp_original is not None:
            # rec_num = st.number_input('Select record to match:',min_value=0,max_value=df_mailchimp_original.shape[0]-1,value=0)
            query = st.selectbox(label = 'User to query for',options = df_mailchimp_original['query'])
            queried_mc_index = int(query.split()[0])
            
            run_query = st.button('Get Results')
        
        #If Run Query Button is pressed, display the parameters of Mail Chimp Record
        if run_query:
            st.header('Searching for member in SAA database')
            st.write(f"First Name: {df_mailchimp_original.loc[queried_mc_index]['First Name']}")
            st.write(f"Last Name: {df_mailchimp_original.loc[queried_mc_index]['Last Name']}")
            st.write(f"Degree: {df_mailchimp_original.loc[queried_mc_index]['Degree']}")
            st.write(f"Email: {df_mailchimp_original.loc[queried_mc_index]['Email Address']}")



# Run the query if button is pressed. Process of running the query
if run_query and df_saa_original is not None:



    # Preprocess the SAA alumni dataframe
    # Filter necessary columns
    df_saa = df_saa_original.filter(['first_name', 'last_name',
                        # 'home_country', 
                        'home_email_address', 'short_degree_string',
                        'bus_email_address', 
                        # 'bus_country', 
                        'email_switch',
                        'saa_email_address', 'gsb_email_address', 'other_email_address'])

    # Replace nulls                    
    df_saa.fillna('n/a',inplace=True)

    #clean column names for easier handling
    for col in df_saa.columns:    
        df_saa[col] = df_saa[col].astype(str).str.lower().str.strip()

    #remove email domains using removeEmailDomain helper function
    email_cols = ['home_email_address', 'bus_email_address', 'email_switch',
                'saa_email_address', 'gsb_email_address', 'other_email_address']
    for email in email_cols:
        df_saa[email] = df_saa[email].apply(removeEmailDomain)

    # Cleaning degree string column using cleanDegreeStr helper function
    df_saa.short_degree_string = df_saa.short_degree_string.apply(cleanDegreeStr)







    # Preprocess the MailChimp dataframe dataframe
    # Filter necessary columns
    df_mailchimp = df_mailchimp_original.filter(['First Name', 'Last Name', 'Email Address',
                                            'Degree', 'Country'])

    # Replace nulls with 'n/a'
    df_mailchimp.fillna('n/a',inplace=True)

    #clean column names for easier handling
    for col in ['First Name','Last Name','Email Address','Degree']:
        df_mailchimp[col] = df_mailchimp[col].str.lower().str.strip()

    #remove email domains using removeEmailDomain helper function
    df_mailchimp['Email Address'] = df_mailchimp['Email Address'].apply(removeEmailDomain)

    # Cleaning degree string column using cleanDegreeStr helper function
    df_mailchimp.Degree = df_mailchimp.Degree.apply(cleanDegreeStr)









    if results_dict is None:
        results_dict = {}
        for i in range(0,df_mailchimp.shape[0]):

            
            user_dict={}
            #map the data of a mailchimp record to the format in SAA df
            df_mapped_mc_rec = map_MailChimpData_to_SAA_DF(i,df_mailchimp)
            
            
            #subsetting the original SAA df by the first name
            df_saa_subset = df_saa[df_saa['first_name'] == df_mapped_mc_rec.iloc[0]['first_name']]
            
            #Concatenating the 2 dataframes together
            df_mc_and_saa_subset = pd.concat([df_mapped_mc_rec,df_saa_subset], axis = 0)            
            
            #Changing degree column to vectorized columns
            df_mc_and_saa_subset = parseDegreeCol(df=df_mc_and_saa_subset,deg_colName='short_degree_string')            

            #one hot encoding our dataframe
            ohe_df = ohe(df_mc_and_saa_subset, df_mc_and_saa_subset.columns)

            #dropping off the columns that have been ohe since they are still present
            ohe_df.drop(columns = df_mc_and_saa_subset.columns, inplace = True)
            
            # setting our y for cosine similarity
            y = np.array(ohe_df.iloc[0])
            y = y.reshape(1,-1)
            
            # using Cosine Similarity
            cos_sim = cosine_similarity(ohe_df, y)
            
            #converting the cosine score array into a df
            cos_sim = pd.DataFrame(data=cos_sim, index=ohe_df.index).sort_values(by=0, ascending=False) #[1:]
            
            #saving the cos_sim index which should be the SAA indexes
            results = list(cos_sim.index)
            
            #locating these indexes in our subset
            results_df = df_mc_and_saa_subset.loc[results]

            # save the cosine df as a value to the cosine_sim_result and the cosine scores. Used primarily for debugging.
            user_dict['cosine_sim_result'] = results_df
            user_dict['cosine_scores'] = cos_sim
            
            #original data that can be found the SAA database that matches with the MailChimp
            user_dict['SAA_query_result'] = df_saa_original.iloc[results[1:]]
            
            
            
            # creates a dictonary 
            results_dict[i] = user_dict

        
            

    st.markdown('### Queried Results from the SAA database:')

    columns = ['first_name','last_name','short_degree_string',
                'home_phone_number','bus_phone_number',
                'home_email_address', 'bus_email_address', 'email_switch',
                'saa_email_address', 'gsb_email_address', 'other_email_address']

    st.dataframe(results_dict[queried_mc_index]['SAA_query_result'].filter(columns).fillna(''))
