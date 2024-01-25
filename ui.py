from tkinter import *
from tkinter import ttk
from main import *
from tkinter.messagebox import showinfo

root = Tk()
root.title("Home library search")
root.geometry("1280x720")
root.pack_propagate(False)
root.resizable(0, 0)

def create_result_window(df):
    window = Tk()
    window.title("Результат агрегации")
    window.geometry("600x400")

    resultTable = ttk.Treeview(window)
    resultTable.place(relheight=1, relwidth=1) 

    treescrolly = Scrollbar(window, orient="vertical", command=resultTable.yview) 
    treescrollx = Scrollbar(window, orient="horizontal", command=resultTable.xview) 
    resultTable.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) 
    treescrollx.pack(side="bottom", fill="x") 
    treescrolly.pack(side="right", fill="y") 

    resultTable["column"] = list(df.columns)
    resultTable["show"] = "headings"
    for column in resultTable["columns"]:
        resultTable.heading(column, text=column) 

    df_rows = df.to_numpy().tolist() 
    for row in df_rows:
        resultTable.insert("", "end", values=row)

def show_raw_data():
    df = return_raw_data()
    show_result(df)
    return None


def show_result(df):
    resultTable.delete(*resultTable.get_children())
    resultTable["column"] = list(df.columns)
    resultTable["show"] = "headings"
    for column in resultTable["columns"]:
        resultTable.heading(column, text=column) 

    df_rows = df.to_numpy().tolist() 
    for row in df_rows:
        resultTable.insert("", "end", values=row)

def click_search():
    value = searchInput.get()

    try:
        value = int(value)
    except ValueError:
        value = value
    
    df = search_by_string(value, searchField.get())
    if df.empty:
        showinfo('Результат', 'Ничего не найдено! Попрбуйте снова')
    show_result(df)

    return None

def filter_outdated_books():
    df = filter_by_date_given_away()
    create_result_window(df)
    return None

def agg_by_category():
    df = sum_by_category()
    create_result_window(df)
    return None

def sum_bad_people():
    df = filter_by_people()
    create_result_window(df)
    return None

def show_genre(event):
    selection = genreSelect.get()
    df = search_by_string(selection, 'Жанр')
    show_result(df)
    return None

# объявление элеменмтов интерфейса  

searchInput = Entry(width=75)
searchBtn = ttk.Button(text='Искать', command=click_search)
showOutdatedBooksBtn = ttk.Button(text='Показать книги отданные больше месяца назад', command=filter_outdated_books)
showGenreSum = ttk.Button(text='Список категорий', command=agg_by_category)
showBadPeople = ttk.Button(text='Список людей, которым отдано > 1 книги', command=sum_bad_people)
searchGroup = ttk.LabelFrame(borderwidth=1, relief=SOLID, padding=[8, 10], text='Параметры поиска')
resultFrame = ttk.LabelFrame(text='Результат поиска')
genreSelect = ttk.Combobox( text='Параметры поиска', values=make_genre_list(), state="readonly")
genreSelectLabel = ttk.Label(text='Показать только жанр:')
resultTable = ttk.Treeview(resultFrame)
treescrolly = Scrollbar(resultFrame, orient="vertical", command=resultTable.yview) 
treescrollx = Scrollbar(resultFrame, orient="horizontal", command=resultTable.xview) 
resultTable.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) 
    
searchField = StringVar(value="Автор")
position = {"padx":6, "pady":6, "anchor":NW}

author_rbtn = ttk.Radiobutton(searchGroup, text="Автор", value="Автор", variable=searchField)
name_rbtn = ttk.Radiobutton(searchGroup, text="Название книги", value="Название", variable=searchField)
year_rbtn = ttk.Radiobutton(searchGroup, text="Год издания", value="Год издания", variable=searchField)
#category_rbtn = ttk.Radiobutton(searchGroup, text="Жанр", value="Жанр", variable=searchField)

# размещение элементов интерфейса в окне

searchBtn.place(x=480, y=17)    
searchInput.place(x=20, y=20)
searchGroup.place(x=20, y=45)
author_rbtn.pack(**position)
name_rbtn.pack(**position)
year_rbtn.pack(**position)
#category_rbtn.pack(**position)
showOutdatedBooksBtn.place(x=200, y=45)
showGenreSum.place(x=200, y=75)
showBadPeople.place(x=200, y=105)
genreSelectLabel.place(x=200, y=140)
genreSelect.place(x=200, y=163)
resultFrame.place(x=10,y=200, width=1260, height=510)
resultTable.place(relheight=1, relwidth=1)
treescrollx.pack(side="bottom", fill="x") 
treescrolly.pack(side="right", fill="y") 

genreSelect.bind("<<ComboboxSelected>>", show_genre)

show_raw_data()

root.mainloop()