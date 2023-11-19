import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import messagebox
import pymysql
import os
import shutil
import db_config_file
from dbfunctions import *
import pymysql.cursors
import db_config_file

rows = None
num_of_rows = None
row_counter =0
num_of_rows_s = None
row_counter_2 =0
blank_textboxes_tab_two = True

#========= some database functions===========

class DatabaseError(Exception):
    pass

def open_database():
    try:
        con = pymysql.connect(host=db_config_file.DB_SERVER,
                      user=db_config_file.DB_USER,
                      password=db_config_file.DB_PASS,
                      database=db_config_file.DB,
                      port=db_config_file.DB_PORT)

    except pymysql.InternalError as e:
        raise DatabaseError
    except pymysql.OperationalError as e:
        raise DatabaseError
    except pymysql.NotSupportedError as e:
        raise DatabaseError

    finally:
        return con

def query_database(con, sql, values):
    try:
        cursor = con.cursor()
        cursor.execute(sql, values)
        rows = cursor.fetchall()
        num_of_rows = cursor.rowcount

    except pymysql.InternalError as e:
        raise DatabaseError
    except pymysql.OperationalError as e:
        raise DatabaseError
    except pymysql.ProgrammingError as e:
        raise DatabaseError
    except pymysql.DataError as e:
        raise DatabaseError
    except pymysql.IntegrityError as e:
        raise DatabaseError
    except pymysql.NotSupportedError as e:
        raise DatabaseError
    finally:
        cursor.close()
        con.close()
        return num_of_rows, rows


# === defining an event  ===============

def on_tab_selected(event):

    global blank_textboxes_tab_two

    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    if tab_text == "Fire Data":
        load_database_results()

    if tab_text == "Loss Data":
        blank_textboxes_tab_two = True

    if tab_text == "Add a Fire":
        blank_textboxes_tab_two = True

# == load database result =======

def load_database_results():
    global rows
    global num_of_rows

    try:
        con = open_database()
    except Exception:
        messagebox.showinfo("Database connection error")
        exit()

    #messagebox.showinfo("Connected to Database", "DB Connection OK")

    try:
        sql = "SELECT * FROM wildfires"
        num_of_rows, rows = query_database(con, sql, None)
    except DatabaseError:
        messagebox.showinfo("Error querying the database")

    return True


def database_error(err):
    messagebox.showinfo("Error", err)
    return False

# === scroll through records

def scroll_forward():
    global row_counter
    global num_of_rows
    if row_counter >= (num_of_rows - 1):
        messagebox.showinfo("Database Error13", "End of database")
    else:
        row_counter = row_counter + 1
        print(row_counter)
        fName.set(rows[row_counter][1])
        fam.set(rows[row_counter][2])
        id.set(rows[row_counter][0])


def scroll_back():
    global row_counter
    global num_of_rows

    if row_counter == 0:

        messagebox.showinfo("Database Errorsb", "Start of database")

    else:
        row_counter = row_counter - 1
        fName.set(rows[row_counter][1])
        fam.set(rows[row_counter][2])
        id.set(rows[row_counter][0])



# ========== search records =======



#=====================more tab 3 --- db menu =======

def load_firename():

    try:
        con = open_database()
    except Exception:
        messagebox.showinfo("Database connection error")
        exit()
    try:
        sql = "SELECT wildfirename FROM wildfires order by wildfirename"
        menu_num_of_rows, m_rows = query_database(con, sql, None)
    except DatabaseError:
        messagebox.showinfo("Error querying the database")
        exit()
    return m_rows

#=========================== Quit button

def _quit():
    form.quit()     # stops mainloop
    form.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


def search_records():

    try:
        con = pymysql.connect(host=db_config_file.DB_SERVER,
                              user=db_config_file.DB_USER,
                              password=db_config_file.DB_PASS,
                              database=db_config_file.DB,
                              port=db_config_file.DB_PORT)
        sql = "SELECT * FROM wildfires"
        print(sql)

        vals = (str(options_var.get()), str(fire_var.get()))
        cursor = con.cursor()
        cursor.execute(sql, str(vals))
        my_rows = cursor.rowcount
        cursor.close()
        con.close()
        print(my_rows)
        print("Total Rows: ", total_rows)
    except:
        print('error')

def select_fires(selectfire):
    con = pymysql.connect(host=db_config_file.DB_SERVER,
                          user=db_config_file.DB_USER,
                          password=db_config_file.DB_PASS,
                          database=db_config_file.DB,
                          port=db_config_file.DB_PORT)
    sql = "SELECT wildfirename, acresburned FROM wildfires WHERE wildfirename LIKE '%" +selectfire+"%'"
    data = pd.read_sql(sql, con)
    print(data)
    return data
def select_fires2():
    con = pymysql.connect(host=db_config_file.DB_SERVER,
                          user=db_config_file.DB_USER,
                          password=db_config_file.DB_PASS,
                          database=db_config_file.DB,
                          port=db_config_file.DB_PORT)
    sql = "SELECT * FROM wildfires"
    data = pd.read_sql(sql, con)
    return data

def show_losses():
    con = pymysql.connect(host=db_config_file.DB_SERVER,
                          user=db_config_file.DB_USER,
                          password=db_config_file.DB_PASS,
                          database=db_config_file.DB,
                          port=db_config_file.DB_PORT)
    sql = "SELECT * FROM structuredestroyed"
    data = pd.read_sql(sql, con)
    return data

def show_structures(selectfire):
    con = pymysql.connect(host=db_config_file.DB_SERVER,
                          user=db_config_file.DB_USER,
                          password=db_config_file.DB_PASS,
                          database=db_config_file.DB,
                          port=db_config_file.DB_PORT)
    sql = "SELECT * FROM structuredestroyed WHERE wildfirename LIKE '%" + selectfire +"%'"
    print(sql)
    data = pd.read_sql(sql, con)
    print(data)
    return data

def fire_chart(root,selectfire):
    figure = plt.Figure(figsize=(12, 6), dpi=100)
    plt.xticks(rotation=90)
    ax = figure.add_subplot(111)
    ax.set_title("Wildfire Acres burned")
    ax.set_ylabel("Acres Burned")
    chart_type = FigureCanvasTkAgg(figure, root)
    chart_type.get_tk_widget().pack()
    df = select_fires(selectfire).groupby('wildfirename').sum()
    df.plot(kind='bar', legend=True, ax=ax, rot=0)


def structure_chart(root,selectfire):
    figure = plt.Figure(figsize=(14, 5), dpi=100)
    ax = figure.add_subplot(111)
    ax.set_xlabel("Level of Damage")
    ax.set_ylabel("Structures Affected")
    chart_type = FigureCanvasTkAgg(figure, root)
    chart_type.get_tk_widget().pack()
    df = show_structures(selectfire).groupby('damagelevel')['wildfirename'].value_counts().unstack(fill_value=0)
    print(df)
    df.plot(kind='bar', legend=True, ax=ax, rot=0)
    ax.set_title('Structures Destroyed by Wildfire')

def struct_chart(root,selectfire):
    figure = plt.Figure(figsize=(14, 5), dpi=100)
    ax = figure.add_subplot(111)
    ax.figure.subplots_adjust(left=.1, bottom=.5)
    ax.set_xlabel("Level of Damage")
    ax.set_ylabel("Structures Affected")
    chart_type = FigureCanvasTkAgg(figure, root)
    chart_type.get_tk_widget().pack()
    df = show_structures(selectfire).groupby(['structuretype', 'damagelevel'])['structuretype'].count().unstack('damagelevel').fillna(0)
    print(df)
    df.plot(kind='bar', legend=True, ax=ax, rot=90)
    ax.set_title('Structure Type Impacted by Wildfire')

def city_chart(root,selectfire):
    figure = plt.Figure(figsize=(14, 5), dpi=100)
    ax = figure.add_subplot(111)
    ax.set_xlabel("Level of Damage")
    ax.set_ylabel("Structures Affected")
    chart_type = FigureCanvasTkAgg(figure, root)
    chart_type.get_tk_widget().pack()
    df = show_structures(selectfire).groupby('damagelevel')['structurecity'].value_counts().unstack(fill_value=0)
    print(df)
    df.plot(kind='bar', legend=True, ax=ax, rot=0)
    ax.set_title('Structures Destroyed, by City')

def select_byfire():
    con = pymysql.connect(host=db_config_file.DB_SERVER,
                          user=db_config_file.DB_USER,
                          password=db_config_file.DB_PASS,
                          database=db_config_file.DB,
                          port=db_config_file.DB_PORT)
    sql = "SELECT * FROM wildfires"
    data = pd.read_sql(sql, con)
    fires = data.wildfirename.unique().tolist()
    return fires

def search_records_fire(wildfirename):
    try:
        con = open_database()
    except Exception:
        messagebox.showinfo("Database connection error")
        exit()

    try:
        sql = "SELECT structureaddress, structurecity, wildfirename from structuredestroyed where wildfirename LIKE %s"
        value = wildfirename
        num_of_rows_g, rows_g = query_database(con, sql, value)
        print(con,sql,value)
    except DatabaseError:
        messagebox.showinfo("Error querying the database")
        raise Exception

    return rows_g, num_of_rows_g


def display_query_results():

    try:
        rows, num_of_rows = search_records_fire(fire_var.get())
        print(fire_var.get())
        success = True

    except Exception as e:
        print(e)
        messagebox.showinfo("Tkinter", "Database error11")
        raise Exception


    table = ttk.Treeview(tab3, columns=(1, 2, 3), height=10, show="headings")

    table.heading(1, text="Wildfire Name")
    table.heading(2, text="Acres burned")
    table.heading(3, text="Year")


    table.column(1, width=90)
    table.column(2, width=90)
    table.column(3, width=90)


    table.grid(row=1, column=0, columnspan=3, padx=15, pady=15)

    if success:
        if num_of_rows == 0:
            messagebox.showinfo("Database Error12" "No Results")
        else:
            for row in rows:
                print(row)
                table.insert('', 'end', values=(row[0], row[1], row[2]))






# ==== form code ============
import pandas as pd
import numpy as np
from pandastable import Table, TableModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


form = tk.Tk()

form.title("Wildfire Losses")
form.geometry("800x800")
tab_parent = ttk.Notebook(form)

# Style: https://www.programcreek.com/python/example/104109/tkinter.ttk.Notebook Number 25
style = ttk.Style()
style.theme_create('pastel', settings={
    ".": {
        "configure": {
            "background": '#d8e2dc',  # All except tabs
            "font": 'red'
        }
    },
    "TNotebook": {
        "configure": {
            "background": '#848a98',  # Your margin color
            "tabmargins": [2, 5, 0, 0],  # margins: left, top, right, separator
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": '#fec89a',  # tab color when not selected
            "padding": [10, 2],
            # [space between text and horizontal tab-button border, space between text and vertical tab_button border]
            "font": "white"
        },
        "map": {
            "background": [("selected", '#ffd7ba')],  # Tab color when selected
            "expand": [("selected", [1, 1, 1, 0])]  # text margins
        }
    }
})
style.theme_use('pastel')

# Add Tabs

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)

# Add tables to tabs
tab1.pack()
pt = Table(tab1)
pt.updateModel((TableModel(select_fires2())))
pt.show()

tab2.pack()
pt = Table(tab2)
pt.updateModel((TableModel(show_losses())))
pt.show()

# Bind tabs to notebook
tab_parent.bind("<<NotebookTabChanged>>", on_tab_selected)

tab_parent.add(tab4, text="Summarize Fire Data")
tab_parent.add(tab1, text="Fire Data")
tab_parent.add(tab2, text="Loss Data")


# ====== SET UP STRING VARS =========

fName = tk.StringVar()
fam = tk.StringVar()
id = tk.StringVar()


# === widgets for TAB THREE ================================

# Drop down menu
#dbmenuList = load_firename()
#fire_var = tk.StringVar()
#options_var = tk.StringVar()
#options_var.set("Fire Name")
#db_dropdown = tk.OptionMenu(tab3, fire_var, *tuple(dbmenuList))


#contents = tuple(select_byfire())
#print(*tuple(contents))
#options_var = tk.StringVar()
#options_var.set(contents[0])
#dropdown = tk.OptionMenu(tab3, options_var, *contents)

#====== drop down menu, search button, forward and backward button ==========

#buttonSearchdbMenu = tk.Button(tab3, text="Search", command=display_query_results)
#print(display_query_results)
#buttonSearchList = tk.Button(tab3, text="Search", command=search_records_fire)

#buttonQuit = tk.Button(master=tab3, text="Quit", command=_quit)

#====== arrange label, dropdown menu and button on grid ==========
#db_dropdown.grid(row=0, column=0, padx=15, pady=15)
#buttonSearchdbMenu.grid(row=0, column=1, padx=15, pady=15)


#dropdown.grid(row=0, column=2, padx=15, pady=15)
#buttonSearchList.grid(row=0, column=1, padx=15, pady=15)
#buttonQuit.grid(row=0, column=6, padx=15, pady=15)



# Summary tab

def structuretab():
    tab5 = ttk.Frame(tab_parent)
    tab_parent.add(tab5, text="Summary - Structure Damage")
    tab_parent.select(tab5)
    structure_chart(tab5,selectfire)

def firetab():
    tab5 = ttk.Frame(tab_parent)
    tab_parent.add(tab5, text="Summary - Wildfire")
    tab_parent.select(tab5)
    fire_chart(tab5,selectfire)

def structtab():
    tab5 = ttk.Frame(tab_parent)
    tab_parent.add(tab5, text="Summary - Wildfire")
    tab_parent.select(tab5)
    struct_chart(tab5,selectfire)

def citytab():
    tab5 = ttk.Frame(tab_parent)
    tab_parent.add(tab5, text="Summary - Wildfire")
    tab_parent.select(tab5)
    city_chart(tab5, selectfire)


def command():
    print(clicked.get())
    label.config(text=clicked.get())



options = select_byfire()
clicked = tk.StringVar(tab4)
# initial menu text
clicked.set(clicked.get())

def callback(selection):
    global selectfire
    selectfire = selection

# Create Dropdown menu
drop = tk.OptionMenu(tab4, clicked, *options, command=callback)
drop.grid(row=2, column=0, padx=5, pady=15)



# Create button to change label text
button = tk.Button(tab4, text="Select", command=command)
button.grid(row=2, column=1, padx=15, pady=15)





# Create Label and buttons for summary tab
label = tk.Label(tab4, text="<- Select fire in dropdown, then click Select")
label.grid(row=2, column=3, padx=15, pady=15)

b4_fire = tk.Button(tab4, text="Summarize Fire Acres Burned", command=firetab)
b4_fire.grid(row=3, column=0, padx=15, pady=15)

b4_structure = tk.Button(tab4, text="by Damage Level", command=structuretab)
b4_structure.grid(row=3, column=1, padx=10, pady=10)

b4_stype = tk.Button(tab4, text="by Structure Type", command=structtab)
b4_stype.grid(row=3, column=2, padx=10, pady=10)

b4_city = tk.Button(tab4, text="by City", command=citytab)
b4_city.grid(row=3, column=3, padx=10, pady=10)

tab_parent.pack(expand=1, fill='both')
form.mainloop()