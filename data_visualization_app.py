import streamlit as st
import plotly_express as px
import pandas as pd

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("Interactive Visualiser")

# Add a sidebar
st.sidebar.subheader("Customisation")

# Setup file upload
#uploaded_file = st.sidebar.file_uploader(label="Upload your CSV or Excel file. (200MB max)", type=['csv', 'xlsx'])

global df
#df = pd.read_excel('data/jpol_polrt.xlsx')
df = pd.read_excel('data/journalists_data_all.xlsx')
#if uploaded_file is not None:
#    print(uploaded_file)
#    print("File uploaded successfully!")

#    try:
#        df = pd.read_csv(uploaded_file)
#    except Exception as e:
#        print(e)
 #       df = pd.read_excel(uploaded_file)

global numeric_columns
global non_numeric_columns
try:
    df = df[['username','followers','total','bjp_pol','inc_pol','other_pol','party']]
    st.write(df)
    journalists = list(df['username'])
    journalists.insert(0,'Select All')

    # select to viz    
    options = st.multiselect(
    'Select journalists to visualise:',
    journalists,
    [journalists[1], journalists[2]])
    #st.write('You selected:', options)

    if 'Select All' in options:
        options = journalists[1:]

    df = df[df['username'].isin(options)]

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
        x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
        color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
        size_value = st.sidebar.selectbox("Size", options=numeric_columns)
        plot = px.scatter(data_frame=df, x=x_values, y=y_values, color=color_value, size=size_value, hover_name="username")
        # display the chart
        st.plotly_chart(plot)
    except Exception as e:
        print(e)