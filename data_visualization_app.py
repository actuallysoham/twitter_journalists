import streamlit as st
import plotly_express as px
import pandas as pd

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("Interactive Visualiser")

# Add a sidebar
st.sidebar.subheader("Customisation")

global df
#df = pd.read_excel('data/jpol_polrt.xlsx')
df = pd.read_excel('data/journalists_data_all.xlsx')

global numeric_columns
global non_numeric_columns
try:
    df = df[['username','followers','total','bjp_pol','inc_pol','other_pol','party']]
    df.rename(columns = {'username':'Twitter Username','followers':'Total number of followers on Twitter','total':'Total number of RTs received from politicians', 'bjp_pol':'BJP vs Others (Binary Polarity)','inc_pol':'INC vs Others (Binary Polarity)','other_pol':'Others vs BJP + INC (Binary Polarity)','party':'Inferred Political Leaning'}, inplace = True)
    full_df = df
    journalists = list(df['Twitter Username'])
    journalists.insert(0,'Select All')

    # select to viz    
    options = st.multiselect(
    'Select journalists to visualise:',
    journalists,
    [journalists[1], journalists[2], journalists[3]])
    #st.write('You selected:', options)

    if 'Select All' in options:
        options = journalists[1:]

    df = df[df['Twitter Username'].isin(options)]

    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    non_numeric_columns = list(df.select_dtypes(['object']).columns)
    #non_numeric_columns.append(None)
    #print(non_numeric_columns)
    

except Exception as e:
    print(e)
    st.write("Please upload file to the application.")

# add a select widget to the side bar
chart_select = st.sidebar.selectbox(
    label="Select the chart type",
    options=['Scatterplots']
)

if chart_select == 'Scatterplots':
    st.sidebar.subheader("Scatterplot Settings")
    try:
        x_values = st.sidebar.selectbox('X axis', options=numeric_columns, index=2)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns, index=1)
        color_value = st.sidebar.selectbox("Color", options=non_numeric_columns, index=1)
        size_value = st.sidebar.selectbox("Size", options=numeric_columns, index=0)
        plot = px.scatter(data_frame=df, x=x_values, y=y_values, color=color_value, size=size_value, hover_name="Twitter Username")
        # display the chart
        st.plotly_chart(plot)
        st.caption('Figure: Political reception of Indian Journalists as inferred from RTs from politicians (Aug 2021 - Sept 2022)')
    except Exception as e:
        print(e)

    #st.header('Full Dataset')
    #st.write(full_df)
    st.subheader('Note on Polarity Scores')
    st.write('The polarity scores are calculated by a simple ratio of RTs received by a journalist from politicians and their affiliations. Tweets were collected over a period starting from 1st August 2021 to 14th September 2022. Please refer to the original blogpost (http://joyojeet.people.si.umich.edu/journalists/) for additional details on the data collection process, methodology and interpretation.')
    st.write('Also note that these scores are a crude approximation, subject to various levels of errors. They should not be treated as a robust or accurate indicator of political affiliation')
    
