import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.title('国勢調査')
st.text('このアプリは国勢調査の結果を指定した条件で表示します')
st.text('左のサイドバーから条件を指定してください')
st.divider()

df = pd.read_csv('kokusei.csv')

with st.sidebar:
    option = st.radio('見たい結果を選択してください',
                      ['人口推移','人口比較'])
    st.divider()
    selected_prefectures = st.multiselect('都道府県を選択してください',
                                          df['都道府県名'].unique())
    selected_label = st.selectbox('性別を選択してください',
                                    ['男','女','男＆女'])
    if selected_label == '男':
         selected_sex = '人口（男）'
    elif selected_label == '女':
         selected_sex = '人口（女）'
    elif selected_label == '男＆女':
        selected_sex = '人口（総数）'
    
    if option == '人口比較':
         selected_year = st.selectbox('年を選択してください',
                                        df['西暦（年）'].unique())
     
    st.info('条件を変えると自動でグラフが更新されます。')

df = df[df['都道府県名'].isin(selected_prefectures)]
if option == '人口比較':
     df = df[df['西暦（年）'] == selected_year]

if not selected_prefectures:
    st.warning('左側のサイドバーから都道府県を選択してください。')
    st.stop()

if option == '人口推移':
     fig = px.line(df,
                   x='西暦（年）',
                   y=selected_sex,
                   color='都道府県名',
                   labels={selected_sex:'人口 単位：人','西暦（年）':'西暦(年) 単位：年'},  
                   title = f'{selected_sex}の人口推移')
     st.plotly_chart(fig)

if option == '人口比較':
     fig = px.bar(df,
                   x='都道府県名',
                   y=selected_sex,
                   color='都道府県名',
                   labels={selected_sex:'人口 単位：人','都道府県名':''},
                   title = f'{selected_year}年：{selected_sex}の都道府県別人口比較')
     st.plotly_chart(fig)

st.caption('出典：総務省統計局「国勢調査」のデータを使用して作成')
st.dataframe(df)