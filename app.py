import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Pesquisa de satisfação')

# --- DISPLAY LOGO Schneider & HEADERS
col1, col2 = st.columns([1, 3])

with col1:
        st.image("images/icon-120.png")

with col2:
        st.header('Satisfação com a temperatura dos ambientes')
        st.subheader('Analise das respostas dos usuários')

# --- Open Excel File
excel_file = '1Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:E',
                   header=3)

df_participants = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='F:G',
                                header=3)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
department = df['Departamento'].unique().tolist()
ages = df['Idade'].unique().tolist()
gender = df['Sexo'].unique().tolist()

age_selection = st.slider('Filtrar por idade:',
                        min_value= min(ages),
                        max_value= max(ages),
                        value=(min(ages),max(ages)))



department_selection = st.multiselect('Filtrar por departamento:',
                                    department,
                                    default=department)

gender_selection = st.multiselect('Filtrar por sexo:',gender,default=gender)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Idade'].between(*age_selection)) & (df['Departamento'].isin(department_selection)) & (df['Sexo'].isin(gender_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Numero de respostas disponíveis: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Rating']).count()[['Idade']]
df_grouped = df_grouped.rename(columns={'Idade': 'Votes'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence = ['#ffffff']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
image = Image.open('images/survey.jpg')
col1.image(image,
        caption='Aplication made by Marcos Felicio',
        use_column_width=True)
col2.dataframe(df[mask])