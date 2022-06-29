from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

import regex as re
import pandas as pd
import numpy as np
import random 
# import pycountry
np.random.seed = 42
random.seed(42)


def removeEmailDomain(email):
    '''
    removes the email portion of an email.
    Ex. xxxx@gmail.com becomes xxxx
    '''
    email = str(email)
    #if email string contains @ symbol return the handle
    if email.find('@')>-1:
        return email.split('@')[0]
    else:
        return 'n/a'


# def mapCountry(countryStr):
#     '''
#     Maps a Country
#     '''
#     if countryStr not in [np.nan, None, 'nan','*', '','N/A','n/a']:
#         return pycountry.countries.search_fuzzy(countryStr)[0].alpha_3
#     return 'n/a'

def ohe(df, column): 
    '''
    Converts the strings in a column into their own columns
    '''
    for col in column:
        train = df[[col]]
        ohe = OneHotEncoder(sparse=False, handle_unknown="error")
        ohe.fit(train)
        encoded_train = ohe.transform(train)
        col_names = [f"{col}_{f}" for f in ohe.get_feature_names()]
        encoded_train = pd.DataFrame(encoded_train,
                                     columns=col_names, index=df.index)
        df = pd.concat([df, encoded_train], axis=1)
        
    return df

def parseDegreeCol(df,deg_colName='short_degree_string'):
    '''
    CountVectorizes the degree columns in a given databse
    '''
    vectorizer = CountVectorizer()
    
    t = vectorizer.fit_transform(df[deg_colName])
    
    # Remove original degree column from original dataframe
    df = df.drop(columns=[deg_colName])
    
    # Create new vectorized degree columns and concatenate
    deg_df =  pd.DataFrame(t.toarray(),columns=vectorizer.get_feature_names(),index = df.index)
    if 'nan' in deg_df.columns:
        deg_df.drop(columns = 'nan')
    return pd.concat([df,deg_df],axis = 1).fillna(0)

def cleanDegreeStr(degree):
    '''
    Clean the degree strings to allow for better handling
    '''
    no_nums_puncs = re.sub('[;,\'*0-9]', ' ', degree).strip()
    return re.sub('[ ]+', ' ', no_nums_puncs).strip()


def map_MailChimpData_to_SAA_DF(mc_rec_idx,df_mc):
    '''
    Creates a SAA df for the mailchimp individual. Because SAA has multiple
    fields for email addresses and mailchimp only has one. The one email is then
    filled in for all the different email addresses.
    
    '''
    mc_rec = df_mc.iloc[mc_rec_idx]
    target_dict = {
        'first_name': mc_rec['First Name'], 
        'last_name': mc_rec['Last Name'],

        # 'home_country': mc_rec['Country'],  
        'home_email_address': mc_rec['Email Address'],    

        'short_degree_string': mc_rec['Degree'],

        'bus_email_address': mc_rec['Email Address'],
        # 'bus_country': mc_rec['Country'],

        'email_switch': mc_rec['Email Address'],
        'saa_email_address': mc_rec['Email Address'],
        'gsb_email_address': mc_rec['Email Address'],
        'other_email_address': mc_rec['Email Address']
        }
    return  pd.DataFrame(target_dict,index=['mc_'+str(mc_rec_idx)])



 