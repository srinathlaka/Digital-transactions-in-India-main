import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot 
import plotly.express as px
import plotly.graph_objs as go
st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(layout="wide")
# title 
st.title('Digital transactions in India using Phonepe')
st.write('  ') #To create space between title and slect box

    ### Map transactions statewise
st.header('Statewise transactions in Millions')
map_data =pd.read_csv('csv_files/map_data.csv')
col1, col2 = st.columns(2)
years = map_data['Year'].unique()#extracting years from dataframe
Quarters = map_data['Quarter'].unique()#extracting quarters from dataframe
#select box to choose year and quarter
with col1:
    year_choice = st.selectbox('Year', years, key=10)
with col2:
    quarter_choice = st.selectbox('Quarter', Quarters, key=11)
st.write(' ')
st.write(' ')
selected_df1 = map_data[(map_data ['Quarter'] == quarter_choice) & (map_data ['Year'] == year_choice)]
fig1=(px.choropleth(selected_df1, 
            locations= 'States', 
            geojson= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", 
            featureidkey= 'properties.ST_NM',
            color= 'Amount in Millions',
            color_continuous_scale='viridis'))
fig1.update_geos(fitbounds= "locations", visible= False)
fig1.update_layout( height=600, width=1400)
        
with st.container():
    st.plotly_chart(fig1, use_container_width=True)

################################################################

###Aggregated transactions statewise
st.header('Statewise transactions based on payment type')
aggr_states_trans =pd.read_csv('csv_files/transactions_states.csv')
duplicates = aggr_states_trans.duplicated(keep=False)
col1, col2, col3 = st.columns(3)
years = aggr_states_trans['Year'].unique()#extracting years from dataframe
Quarters = aggr_states_trans['Quarter'].unique()#extracting quarters from dataframe
Payment_type=aggr_states_trans['Payment_type'].unique()#extracting type of payment from dataframe
#select box to choose year and quarter
with col1:
    year_choice = st.selectbox('Year', years, key=6)
with col2:
    quarter_choice = st.selectbox('Quarter', Quarters, key=7)
with col3:

    payment_choice = st.selectbox('Payment Type', Payment_type, key=109)
st.write(' ')
st.write(' ')
selected_df = aggr_states_trans[(aggr_states_trans['Quarter'] == quarter_choice) & (aggr_states_trans['Year'] == year_choice)&
                                (aggr_states_trans['Payment_type'] == payment_choice)]
# Creating the map
with st.container():
    fig2= px.choropleth(selected_df, 
                    locations= 'States', 
                    geojson= 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson', 
                    featureidkey= 'properties.ST_NM',
                    color= 'Amount in Millions',
                    scope = 'asia', 
                    hover_name= 'States',
                    hover_data= [ "Transaction_count", "Amount in Millions"],
                    color_continuous_scale='Viridis')
    fig2.update_geos(fitbounds= "locations", visible= False)
    fig2.update_layout( height=600, width=1400)
    st.plotly_chart(fig2, use_container_width=True)

################################################################
###Top states


st.header('Top 10 transactions for States')
top_states=pd.read_csv('csv_files/top_states.csv')
col1, col2 = st.columns(2)
years = top_states['Year'].unique()#extracting years from dataframe

Quarters = top_states['Quarters'].unique()#extracting quarters from dataframe

#select box to choose year, district and quarter


with col1:
    year_choice = st.selectbox('Year', years, key=2)

with col2:
    quarter_choice = st.selectbox('Quarter', Quarters, key=3)

st.write(' ')
st.write(' ')
col1, col2, col3 = st.columns((1,2,1), gap='large')

with col1:
    # Filtering the DataFrame to include only data for the selected district and year
    selected_df = top_states[(top_states['Quarters'] == quarter_choice) & (top_states['Year'] == year_choice)]

    # Select only the "Districts", "Amount" and "count" columns
    amount_df = selected_df[['States', 'Amount in Millions', 'Transaction_count']]
    #selected_df.index = selected_df.reset_index().index + 1
    #selected_df = selected_df.sort_values('Transaction_count', ascending=True)
    amount_df.index = amount_df.reset_index().index + 1
    amount_df.drop(columns='Transaction_count', inplace=True)

    # Display the resulting DataFrame
    st.write(amount_df)
    

with col2:
    st.bar_chart(data=selected_df, x='States', y='Transaction_count')

with col3:
    st.subheader('Observations')
    st.write('* Telangana and Maharashtra are consistently the top two states in terms of amount in millions across all years.')
    st.write('* The total amount in millions for all states increases each year, which indicate overall growth of digital payments in India.')
    st.write('* Karnataka, Andhra Pradesh, Rajasthan, Uttar Pradesh, Madhya Pradesh, Bihar and Delhi appear in the top ten states with the highest amount of transactions in multiple years.')

################################################################
#Top Districts
st.header('Top 10 transactions for Districts')
#Top districts 
top_districts=pd.read_csv('csv_files/top_districts.csv')
col1, col2 = st.columns(2)
years = top_districts['Year'].unique()#extracting years from dataframe

Quarters = top_districts['Quarters'].unique()#extracting quarters from dataframe

#select box to choose year, district and quarter


with col1:
    year_choice = st.selectbox('Year', years)

with col2:
    quarter_choice = st.selectbox('Quarter', Quarters, key=0)

st.write(' ')
st.write(' ')
col1, col2, col3 = st.columns((1,2,1), gap='large')

with col1:
    # Filtering the DataFrame to include only data for the selected district and year
    selected_df = top_districts[(top_districts['Quarters'] == quarter_choice) & (top_districts['Year'] == year_choice)]

    # Select only the "Districts", "Amount" and "count" columns
    amount_df = selected_df[['Districts', 'Amount in Millions', 'Transaction_count']]
    #selected_df.index = selected_df.reset_index().index + 1
    #selected_df = selected_df.sort_values('Transaction_count', ascending=True)
    amount_df.index = amount_df.reset_index().index + 1
    amount_df.drop(columns='Transaction_count', inplace=True)

    # Display the resulting DataFrame
    st.write(amount_df)
    

with col2:
    st.bar_chart(data=selected_df, x='Districts', y='Transaction_count')

with col3:
    st.subheader('Observations')
    st.write('* Bengaluru urban almost consistently tops the list.')
    st.write('* In 2022, Hyderabad crosses Bengaluru urban in both Amount transferred and Transactions made.')
    st.write('* There is a overall increase in trend for both Amount transferred and Transactions.')


################################################################
#Top Pincodes
st.header('Top 10 transactions for Pincodes')
#Top Pincodes
top_pincodes=pd.read_csv('csv_files/top_pincodes.csv')
col1, col2 = st.columns(2)
years = top_pincodes['Year'].unique()#extracting years from dataframe

Quarters = top_pincodes['Quarters'].unique()#extracting quarters from dataframe

#select box to choose year, Pincodes and quarter


with col1:
    year_choice = st.selectbox('Year', years, key=5)

with col2:
    quarter_choice = st.selectbox('Quarter', Quarters, key=4)

st.write(' ')
st.write(' ')
col1, col2, col3 = st.columns((1,2,1), gap='large')

with col1:
    # Filtering the DataFrame to include only data for the selected Pincodes and year
    selected_df = top_pincodes[(top_pincodes['Quarters'] == quarter_choice) & (top_pincodes['Year'] == year_choice)]

    # Select only the "Pincodes", "Amount" and "count" columns
    amount_df = selected_df[['Pincodes', 'Amount in Millions', 'Transaction_count']]

    amount_df.index = amount_df.reset_index().index + 1
    amount_df.drop(columns='Transaction_count', inplace=True)

    # Display the resulting DataFrame
    st.write(amount_df)
    

with col2:
    st.bar_chart(data=selected_df, x='Pincodes', y='Transaction_count')

with col3:
    st.subheader('Observations')
    st.write('* Overall, the top pin codes in terms of transaction amount seem to be concentrated in areas of high economic activity, such as major metropolitan cities.')
    st.write('* Pincode 500,001 appears in all the years and has consistently high transaction amounts.')








    ###Aggregated transactions 
st.header('Aggregated transactions based on payment type')
aggr_trans =pd.read_csv('csv_files/Transaction_count.csv')
col1, col2 = st.columns(2)
years = aggr_trans['Year'].unique()#extracting years from dataframe
Quarters = aggr_trans['Quarter'].unique()#extracting quarters from dataframe
#select box to choose year and quarter
with col1:
    year_choice = st.selectbox('Year', years, key=8)
with col2:
    quarter_choice = st.selectbox('Quarter', Quarters, key=9)
st.write(' ')
st.write(' ')
col1, col2 = st.columns((2,1)) 
selected_df3 = aggr_trans[(aggr_trans ['Quarter'] == quarter_choice) & (aggr_trans ['Year'] == year_choice)]

with col1:
    #select box to choose year and quarter
    #selected_df3 = aggr_trans[(aggr_trans ['Quarter'] == '1st Quarter') & (aggr_trans ['Year'] == 2022)].copy()
    selected_df3['Percentage'] = selected_df3['Transaction_count'] / selected_df3['Transaction_count'].sum() * 100
    threshold = 5  # set the threshold percentage for grouping
    small_slices = selected_df3[selected_df3['Percentage'] < threshold]

    other_slice = pd.DataFrame({
        'Payment_Type': ['Others'],
        'Transaction_count': [small_slices['Transaction_count'].sum()],
        'Percentage': [small_slices['Percentage'].sum()],
        'Amount in Millions': [small_slices['Amount in Millions'].sum()],

    })
    selected_df3 = selected_df3[selected_df3['Percentage'] >= threshold]
    selected_df3=pd.concat([selected_df3,other_slice], axis=0)
    selected_df3['Year'] = 2022
    selected_df3['Quarter'] = '1st Quarter'

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = selected_df3['Payment_Type']
    sizes = selected_df3['Transaction_count']
    #hovertext= selected_df3['Transaction_count']
    #fig1, ax1 = plt.subplots()
    fig3 = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.5, hovertext= selected_df3['Transaction_count'],
                                hovertemplate='<b>%{label}</b><br>' + 'Transaction_count: %{value}<br>' )])
    
    fig3.update_layout( height=600, width=800)

    st.plotly_chart(fig3)


with col2:
    st.subheader('Observations')
    st.write('* Peer-to-peer payments had the highest transaction count in every quarter from 2018 to 2020, followed by Recharge & bill payments and Merchant payments.')
    st.write('* Merchant payments increased their count from second quarter of 2022 and topped the transactions crossing peer to peer transactions.')
    st.write('* Overall, the transaction count for all payment types increased from 2018 to 2022.')




