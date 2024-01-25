import pandas as pd
import datetime as dt
import numpy as np

df = pd.read_excel('data/Books.xlsx')

def return_raw_data():
    return df

def search_by_string(value, column):

    # функция поиска в любом столбце по значению
    # value - значение, str или int 
    # column - название столбца, str

    if isinstance(value, str):
        return df[df[column].str.lower().str.contains(value.lower())]
    if isinstance(value, int):
        return df[df[column].isin([value])]


def search_by_period(year_start, year_finish):

    # функция вывода книг в отрезке по годам
    # year_start - начало отрезка, int
    # year_finish - конец отрезка, int 

    return df[df['Год издания'].between(year_start,year_finish, inclusive='both')]


def filter_by_date_given_away():

    # функция выводит записи о книгах, отданых более месяца назад

    now = dt.datetime.now()
    temp_df = df[df['Когда отдана'].notna()]
    return temp_df[(now.year - temp_df['Когда отдана'].dt.year > 0) | (now.month - temp_df['Когда отдана'].dt.month >= 1)]


def filter_by_people():

    # функция выводит список людей, которым отдано больше 1 книги и количество книг

    subdf = df.groupby('Кому отдана', as_index=False).agg(**{
        "Количество книг": pd.NamedAgg(column="Название", aggfunc="count"),
    })
    return subdf[subdf["Количество книг"] > 1]



def sum_by_category():

    # функция вводит списко жанров с указанием общего количества книг, количества издательств и общего количества страниц

    return df.groupby('Жанр', as_index=False).agg(**{
        "Количество книг": pd.NamedAgg(column="Название", aggfunc="count"),
        "Количество издательств": pd.NamedAgg(column="Издательство", aggfunc="nunique"),
        "Общее количество страниц": pd.NamedAgg(column="Кол-во страниц", aggfunc="sum")
    })

def make_genre_list(): 

    # фунцкия создает списко жанров (для вставки в combobox)

    return list(df['Жанр'].unique())