import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from plotly import express as px

def check_genre(x, kwargs):
    if len(set(x).intersection(set(kwargs['genre_list']))) == 0:
        return False
    else:
        return True

def main():
    # Подготовим данные
    df_raw = pd.read_csv('https://code.s3.yandex.net/datasets/' + 'movies.csv')
    df_raw['genre_prep'] = df_raw['Жанр'].str.strip().str.split(', ') 
    df_raw['Прибыльность, %'] = round(100 * df_raw['Сборы, \$ млн'] / df_raw['Бюджет, \$ млн'], 1)
    
    st.title('Дашборд по фильмам Оскар')

    with st.sidebar:   
        # Фильтры
        budget = st.slider('Бюджет, $ млн',
                           df_raw['Бюджет, \$ млн'].min(),
                           df_raw['Бюджет, \$ млн'].max(),
                           value=(df_raw['Бюджет, \$ млн'].min(), df_raw['Бюджет, \$ млн'].max()))
        income = st.slider('Сборы, $ млн',
                           df_raw['Сборы, \$ млн'].min(),
                           df_raw['Сборы, \$ млн'].max(),
                           value=(df_raw['Сборы, \$ млн'].min(), df_raw['Сборы, \$ млн'].max()))
        length = st.slider('Длина, мин.',
                           df_raw['Длина, мин.'].min(), 
                           df_raw['Длина, мин.'].max(),
                           value=(df_raw['Длина, мин.'].min(), df_raw['Длина, мин.'].max()))

        # Фильтруем диапазоны
        df = df_raw[(df_raw['Бюджет, \$ млн'] >= budget[0]) & (df_raw['Бюджет, \$ млн'] <= budget[1]) \
                & (df_raw['Сборы, \$ млн'] >= income[0]) & (df_raw['Сборы, \$ млн'] <= income[1]) \
                & (df_raw['Длина, мин.'] >= length[0]) & (df_raw['Длина, мин.'] <= length[1])]

        genre_uniq = df_raw['genre_prep'].explode().unique()
        genre_list = st.multiselect('Жанр', tuple(genre_uniq))

        # Фильтруем жанры
        if len(genre_list) != 0:
            df = df[df['genre_prep'].apply(check_genre, kwargs={'genre_list': genre_list})]

    # Строим диаграмму рассеивания
    fig = px.scatter(df,
                     x='Длина, мин.',
                     y='Бюджет, \$ млн',
                     hover_data=['Название'],
                     title='Связь длины фильма и размера бюджета')
    # Диаграмма рассеивания
    st.plotly_chart(fig)
    # Таблица фильмов
    st.table(df[['Название', 'Рейтинг', 'Жанр', 'Прибыльность, %']])

main()