import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff

import plotly.graph_objects as go


st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")
#@st.cache
def get_data_from_excel(file):
    data = pd.read_excel(
        io=file,
        engine="openpyxl"
    )
    return data
Mode = st.multiselect(
                label='Choose what you want to display', options=['Projection', 'Distribution' ]
            )
if Mode == ['Projection']:
    uploaded_file_1 = st.file_uploader("Choose a file", type=['xlsx', 'csv'], key='1')

    if uploaded_file_1 is not None:
        uploaded_file_2 = st.file_uploader("Choose a file", type=['xlsx', 'csv'], key='2')
        if uploaded_file_2 is not None:
            data_1 = get_data_from_excel(uploaded_file_1)
            R = list(data_1.columns)
            del R[0:3]
            data_2 = get_data_from_excel(uploaded_file_2)
            S = list(data_2.columns)
            X = S[0]
            del S[0]
            for i in range(len(R)):
                S[i] = 'CE ' + R[i]
            data_2.columns = [X] + S
            data_1['TVOG/BE N'] = data_1['TVOG N'] / data_1['BE N']
            data_1['TVOG/BE N-1'] = data_1['TVOG N-1'] / data_1['BE N-1']
            L = list(data_1.columns)
            del L[0:3]
            data_3 = data_1.groupby(['Simulation', 'Year']).sum().reset_index(level=[0, 1])
            df = data_3
            data_3['Pool'] = ['Total_Pool'] * len(data_3)
            data_4 = pd.concat([data_1, data_3])
            data_5 = df.groupby(['Year']).mean().reset_index(level=[0])
            data_5['Pool'] = ['STO/CE'] * len(data_5)
            data_5['Simulation'] = ['STO/CE'] * len(data_5)
            data_6 = pd.concat([data_4, data_5])


            def add_logo(logo_path, width, height):
                """Read and return a resized logo"""
                logo = Image.open(logo_path)
                modified_logo = logo.resize((width, height))
                return modified_logo


            my_logo = add_logo(logo_path="Image1.png", width=200, height=200)
            st.sidebar.image(my_logo)
            st.sidebar.header("Filter:")

            Simulation = st.sidebar.multiselect(
                "Choose a Simulation:",
                options=data_6["Simulation"].unique()
            )
            Pool = st.sidebar.multiselect(
                "Choose a Pool:",
                options=data_6["Pool"].unique()
            )
            data_7 = data_6.query(
                '''Simulation == @Simulation & Pool == @Pool'''
            )
            if Simulation == ['STO/CE'] and Pool == ['STO/CE']:
                M = list(data_7.columns)
                P = M[0:3]
                for i in range(len(M)):
                    M[i] = 'STO ' + M[i]
                del M[0:3]
                data_7.columns = P + M
                data_8 = pd.merge(data_7, data_2, on='Year')
                N = list(data_8.columns)
                del N[0:3]
                st.dataframe(data_8)
                st.title(":bar_chart: Dashboard")
                st.markdown("---")

                columns = st.multiselect(
                    label='Choose variable(s) you want to display', options=N
                )

                fig_1 = go.Figure()
                for e in columns:
                    fig_1.add_trace(go.Scatter(x=data_8['Year'], y=data_8[e],
                                                       mode='lines',
                                                       name='Variable = ' + str(e) + '/ Simulation = STO/CE / Pool = STO/CE' ))

                st.plotly_chart(fig_1, use_container_width=True)
                fig_2 = go.Figure()
                for e in columns:
                    fig_2.add_trace(go.Scatter(x=data_8['Year'], y=data_8[e],
                                               mode='lines' , fill='tozeroy',
                                               name='Variable = ' + str(e) + '/ Simulation = STO/CE / Pool = STO/CE'))

                st.plotly_chart(fig_2, use_container_width=True)
                fig_3 = go.Figure()
                for e in columns:
                    fig_3.add_trace(go.Bar(x=data_8['Year'], y=data_8[e],
                                               name='Variable = ' + str(e) + '/ Simulation = STO/CE / Pool = STO/CE'))

                st.plotly_chart(fig_3, use_container_width=True)
                fig_4 = go.Figure()

            else:
                st.dataframe(data_7)
                st.title(":bar_chart: Dashboard")
                st.markdown("---")

                columns = st.multiselect(
                    label='Choose variable(s) you want to display', options=L
                )

                fig_1 = go.Figure()
                for e in columns:
                    for f in Simulation:
                        for j in Pool:
                            data_9 = data_7[data_7['Simulation'] == f]
                            data_10 = data_9[data_9['Pool'] == j]
                            fig_1.add_trace(go.Scatter(x=data_10['Year'], y=data_10[e],
                                                       mode='lines',
                                                       name='Variable = ' + str(e) + ' / Simulation = ' + str(
                                                           f) + ' / Pool = ' + str(j)))

                st.plotly_chart(fig_1, use_container_width=True)
                fig_2 = go.Figure()

                for e in columns:
                    for f in Simulation:
                        for j in Pool:
                            data_9 = data_7[data_7['Simulation'] == f]
                            data_10 = data_9[data_9['Pool'] == j]
                            fig_2.add_trace(go.Scatter(x=data_10['Year'], y=data_10[e],
                                                       mode='lines', fill='tozeroy',
                                                       name='Variable = ' + str(e) + ' / Simulation = ' + str(
                                                           f) + ' / Pool = ' + str(j)))

                st.plotly_chart(fig_2, use_container_width=True)
                fig_3 = go.Figure()
                for e in columns:
                    for f in Simulation:
                        for j in Pool:
                             data_9= data_7[data_7['Simulation'] == f]
                             data_10= data_9[data_9['Pool'] == j]
                             fig_3.add_trace(go.Bar(x=data_10['Year'], y=data_10[e],
                                                   name='Variable = ' + str(e) + ' / Simulation = ' + str(
                                                       f) + ' / Pool = ' + str(j)))
                st.plotly_chart(fig_3, use_container_width=True)

else:
    uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv'])

    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = get_data_from_excel(uploaded_file)
        df['TVOG/BE N'] = df['TVOG N'] / df['BE N']
        df['TVOG/BE N-1'] = df['TVOG N-1'] / df['BE N-1']
        L = list(df.columns)
        del L[0:3]
        Total_Pool = df.groupby(['Simulation', 'Year']).sum().reset_index(level=[0, 1])
        del Total_Pool['Pool']


        def add_logo(logo_path, width, height):
            """Read and return a resized logo"""
            logo = Image.open(logo_path)
            modified_logo = logo.resize((width, height))
            return modified_logo


        my_logo = add_logo(logo_path="Image1.png", width=600, height=600)
        st.sidebar.image(my_logo)

        st.sidebar.header("Filter:")

        Year = st.sidebar.multiselect(
            "Choose a Year:",
            options=Total_Pool["Year"].unique()
        )

        Total_Pool_selection = Total_Pool.query(
            '''Year == @Year'''
        )
        st.dataframe(Total_Pool_selection)
        st.title(":bar_chart: Dashboard")
        st.markdown("---")

        columns = st.multiselect(
            label='Choose variable(s) you want to display', options=L
        )
        fig_1 = go.Figure()
        hist_data = []
        group_labels = []
        bin_size = []
        for e in columns:
            for f in Year :
                data_100 = Total_Pool_selection[Total_Pool_selection['Year'] == f]
                hist_data.append(np.array(data_100[e].values.tolist()))
                group_labels.append('Variable = ' + str(e) + ' / Year = ' + str(f))
        for i in range(len(group_labels)):
            bin_size.append(9700)
        fig = ff.create_distplot(hist_data, group_labels, bin_size)
        st.plotly_chart(fig, use_container_width=True)

