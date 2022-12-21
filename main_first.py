from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont
import engine as en

DB_NAME = 'lab_new'
USER_NAME = 'db_creator'
USER_PASSWORD = ''

cursor = None

try:
    cursor = en.connect_as_user(USER_NAME, USER_PASSWORD, DB_NAME)
except:
    print('database not exists')

def create_database():
    global cursor
    en.create_database(DB_NAME, USER_NAME)
    cursor = en.connect_as_user(USER_NAME, USER_PASSWORD, DB_NAME)
    
def delete_database():
    global cursor
    if cursor is not None:
        en.disconnect_user(cursor)
        en.drop_database(DB_NAME)
        cursor = None

def clear_tables_database():
    if cursor is None:
        return
    en.clear_all_tables(cursor)



def home_page():
    root = Tk()
    root.geometry('1200x750+0+0')
    root.title('БД Турагенства')

    button_font_up = tkFont.Font(family = "Times New Roman", size= 30)
    tours_button = Button(text = "Туры",font = button_font_up, command=tours_page).place(x = 43, y = 127, width = 250, height = 100)
    clients_button = Button(text = "Клиенты",font = button_font_up, command=clients_page).place(x = 334, y = 127, width = 250, height = 100)
    employees_button = Button(text = "Сотрудники",font = button_font_up, command= employees_page).place(x = 625, y = 127, width = 250, height = 100)
    sales_button = Button(text = "Продажи",font = button_font_up, command= sales_page).place(x = 916, y = 127, width = 250, height = 100)

    button_font_down = tkFont.Font(family = "Times New Roman", size= 27)
    create_db = Button(text = "Создать базу данных",font = button_font_down, command= create_database).place(x = 36, y = 462, width=350, height=120 )
    delete_db = Button(text = "Удалить базу данных",font = button_font_down,command= delete_database).place(x = 781, y = 462, width=350, height=120 )
    show_tables = Button(text = "Вывести\nвсе таблицы",font = button_font_up, command= show_all_table).place(x = 459, y = 471, width=250, height=100 )  
    root.mainloop()



def show_all_table():
    show_employees_table()
    show_sales_table()
    show_clients_table()
    show_tours_table()
        
def show_tours_table():

    tours_table = Toplevel()
    tours_table.geometry('1400x200+0+0')
    tours_table.title('Таблица Туры')

    
    tree = ttk.Treeview(tours_table, selectmode='browse')
    tree['columns'] = ('id tour','price','departure dates','departure city','operator','tour duration','country')
    tree.column('#0', width=0, stretch=NO)
    tree.column("id tour", anchor='center')
    tree.column("price", anchor='center')
    tree.column("departure dates", anchor='center')
    tree.column("departure city", anchor='center')
    tree.column("operator", anchor='center')
    tree.column("tour duration", anchor='center')
    tree.column("country", anchor='center')

    tree.heading("id tour",text = "id tour", anchor='center')
    tree.heading("price",text = "price", anchor='center')
    tree.heading("departure dates",text = "departure dates", anchor='center')
    tree.heading("departure city",text = "departure city", anchor='center')
    tree.heading("operator",text = "operator", anchor='center')
    tree.heading("tour duration",text = "tour duration", anchor='center')
    tree.heading("country",text = "country", anchor='center')
    
    scrollbar = Scrollbar(tours_table, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar_2 = Scrollbar(tours_table, orient="horizontal", command=tree.xview)
    scrollbar_2.pack(side=BOTTOM, fill=X)
    
    
    result = en.show_table_tour(cursor)
    print(result)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[3] = values[3][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3]))
  
    
    
    tree.insert(parent='', index=0, iid=0, text='', values=('1','10200','01.01.2001','Moscow','One','6','Russia'))
    tree.pack()

def show_employees_table():

    employees_page = Toplevel()
    employees_page.geometry('800x200+0+200')
    employees_page.title('Таблицы Сотрудники')

    tree = ttk.Treeview(employees_page, selectmode='browse')
    tree['columns'] = ('id employee','full name','number phone','sales quantity')
    tree.column('#0', width=0, stretch=NO)
    tree.column('id employee', anchor='center')
    tree.column('full name', anchor='center')
    tree.column('number phone', anchor='center')
    tree.column('sales quantity', anchor='center')

    tree.heading('id employee',text = 'id employee', anchor='center')
    tree.heading('full name',text = 'full name', anchor='center')
    tree.heading('number phone',text = 'number phone', anchor='center')
    tree.heading('sales quantity',text = 'sales quantity', anchor='center')

    scrollbar = Scrollbar(employees_page, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    result = en.show_table_employee(cursor)
    print(result)

    #нужно объединить функции
    
    tree.insert(parent='', index=0, iid=0, text='', values=('1','Иванов Иван','89563774296','2'))
    tree.pack()

def show_sales_table():

    sales_table = Toplevel()
    sales_table.geometry('800x200+0+400')
    sales_table.title('Таблица Продажи')

    
    tree = ttk.Treeview(sales_table, selectmode='browse')
    tree['columns'] = ('id sale','sale data','id clients','id employees','id tour','total cost')
    tree.column('#0', width=0, stretch=NO)
    tree.column("id sale", anchor='center')
    tree.column("sale data", anchor='center')
    tree.column("id clients", anchor='center')
    tree.column("id employees", anchor='center')
    tree.column("id tour", anchor='center')
    tree.column("total cost", anchor='center')

    tree.heading("id sale",text = "id sale", anchor='center')
    tree.heading("sale data",text = "sale data", anchor='center')
    tree.heading("id clients",text = "id clients", anchor='center')
    tree.heading("id employees",text = "id employees", anchor='center')
    tree.heading("id tour",text = "id tour", anchor='center')
    tree.heading("total cost",text = "total cost", anchor='center')
    
    
    scrollbar = Scrollbar(sales_table, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar_2 = Scrollbar(sales_table, orient="horizontal", command=tree.xview)
    scrollbar_2.pack(side=BOTTOM, fill=X)
    
    #нужно объединить функции
    result = en.show_table_sale(cursor)
    print(result)
    
    tree.insert(parent='', index=0, iid=0, text='', values=('1','10.02.2002','1','1','1'))
    tree.pack()

def show_clients_table():

    clients_table = Toplevel()
    clients_table.geometry('800x200+0+600')
    clients_table.title('Таблицы Клиенты')

    tree = ttk.Treeview(clients_table, selectmode='browse')
    tree['columns'] = ('id clients','full name','number phone','passport','discount')
    tree.column('#0', width=0, stretch=NO)
    tree.column('id clients', anchor='center')
    tree.column('full name', anchor='center')
    tree.column('number phone', anchor='center')
    tree.column('passport', anchor='center')
    tree.column('discount', anchor='center')

    tree.heading('id clients',text = 'id clients', anchor='center')
    tree.heading('full name',text = 'full name', anchor='center')
    tree.heading('number phone',text = 'number phone', anchor='center')
    tree.heading('passport',text = 'passport', anchor='center')
    tree.heading('discount',text = 'discount', anchor='center')
    
    scrollbar = Scrollbar(clients_table, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    #нужно объединить функции
    
    result = en.show_table_client(cursor)
    print(result)
    tree.insert(parent='', index=0, iid=0, text='', values=('1','Иванов Иван','89563774296','2'))
    tree.pack()

def tours_page():
    
    def butt_update_tour():
        en.update_tour(cursor,cell_id_tour.get(),cell_price.get(),cell_data_tour.get()
                        ,cell_departure_city.get(),cell_tour_operator.get(),cell_duration.get(),cell_country.get())

    
    if cursor is None:
        return
    
    def butt_add_to_tour():
        print(cell_id_tour.get(),cell_price.get(),cell_data_tour
                        ,cell_departure_city,cell_tour_operator,cell_duration,cell_country)
    
        en.add_to_tour(cursor,cell_id_tour.get(),cell_price.get(),cell_data_tour.get(),
                       cell_departure_city.get(),cell_tour_operator.get(), cell_duration.get(),cell_country.get())

    def butt_delete_row():
        en.delete_tour_by_id(cursor,cell_id_tour_del.get())
        
    def find_id_tour():
        en.search_tour_by_id(cell_id_tour_find.get())
    
    tours_page_r = Toplevel()
    tours_page_r.geometry("1200x750")
    button_font_up = tkFont.Font(family = "Times New Roman", size= 13)
    tours_page_r.title('Измение таблицы Туры')
    label1=Label(tours_page_r,text="id тура", font=button_font_up).place(x = 82, y = 45)
    
    cell_id_tour = Entry(tours_page_r,width=157)
    cell_id_tour.place(x = 35, y = 95)
    
    label2 = Label(tours_page_r,text="цена", font=button_font_up).place(x = 250, y = 45)
    cell_price = Entry(tours_page_r,width=144)
    cell_price.place(x = 200, y = 95)
    
    Label(tours_page_r,text="дата\nотправления", font=button_font_up).place(x = 400, y = 34)
    cell_data_tour = Entry(tours_page_r,width=160)
    cell_data_tour.place(x = 359, y = 95)

    Label(tours_page_r,text="город\nотправления", font=button_font_up).place(x = 537, y = 34)
    cell_departure_city = Entry(tours_page_r,width=144)
    cell_departure_city.place(x = 528, y = 95)
    
    Label(tours_page_r,text="тур\nоператор", font=button_font_up).place(x = 717, y = 34)
    cell_tour_operator = Entry(tours_page_r,width=156)
    cell_tour_operator.place(x = 681, y = 95)
    
    
    Label(tours_page_r,text="длительность\nтура", font=button_font_up).place(x = 861, y = 34)
    cell_duration = Entry(tours_page_r,width=154)
    cell_duration.place(x = 846, y = 95)
    
    Label(tours_page_r,text="страна", font=button_font_up).place(x = 1050, y = 45)
    cell_country = Entry(tours_page_r)
    cell_country.place(x = 1009, y = 95)
    
    add_row = Button(tours_page_r,text='Добавить запись', font=button_font_up, command=butt_add_to_tour).place(x = 490, y = 165, width=220, height=45)
    ###
    
    Label(tours_page_r,text="id тура", font=button_font_up).place(x = 63, y = 248)
    cell_id_sale_ch = Entry(tours_page_r,width=170)
    cell_id_sale_ch.place(x = 35, y = 296)
    
    Label(tours_page_r,text="цена", font=button_font_up).place(x = 260, y = 241)
    cell_date_sale_ch = Entry(tours_page_r,width=170)
    cell_date_sale_ch.place(x = 215, y = 296)

    Label(tours_page_r,text="дата\nотправления", font=button_font_up).place(x = 425, y = 241)
    cell_quantity_sales_ch = Entry(tours_page_r,width=170)
    cell_quantity_sales_ch.place(x =396, y = 296)
    
    Label(tours_page_r,text="город\nотправления", font=button_font_up).place(x = 537, y = 241)
    cell_departure_city = Entry(tours_page_r,width=144)
    cell_departure_city.place(x = 528, y = 296)
    
    Label(tours_page_r,text="тур\nоператор", font=button_font_up).place(x = 717, y = 241)
    cell_tour_operator = Entry(tours_page_r,width=156)
    cell_tour_operator.place(x = 681, y = 296)
    
    Label(tours_page_r,text="длительность\nтура", font=button_font_up).place(x = 861, y = 241)
    cell_duration = Entry(tours_page_r,width=154)
    cell_duration.place(x = 846, y = 296)

    Label(tours_page_r,text="страна", font=button_font_up).place(x = 1050, y = 241)
    cell_country = Entry(tours_page_r)
    cell_country.place(x = 1009, y = 296)


    update_row = Button(tours_page_r,text='Обновить запись', font=button_font_up,command= butt_update_tour).place(x = 490, y = 345, width=220, height=45)
    

    Label(tours_page_r,text="id тура", font=button_font_up).place(x = 90, y = 380)
    cell_id_tour_del = Entry(tours_page_r)
    cell_id_tour_del.place(x = 60, y = 410)
    
 
    
    delete_row = Button(tours_page_r,text = "Удалить данные" ,font = button_font_up,command=butt_delete_row).place(x = 55, y = 440)
    
    show_table = Button(tours_page_r,text = "Вывести таблицу", font =button_font_up, command=show_tours_table ).place(x = 395, y = 450)
    clear_table = Button(tours_page_r,text = "Очистить таблицу", font =button_font_up,command=en.clear_tour(cursor)).place(x = 640, y = 450)
    
    Label(tours_page_r,text="id тура", font=button_font_up).place(x = 980 , y = 380)
    cell_id_tour_find = Entry(tours_page_r)
    cell_id_tour_find.place(x = 944, y = 410)
    
    
    #Label(tours_page_r,text="страна", font=button_font_up).place(x = 980 , y = 300)
    #cell_id_tour_find = Entry(tours_page_r).place(x = 944, y = 347)
    
    
    ##доделать
    find_row = Button(tours_page_r,text = "Найти запись" ,font = button_font_up, command=find_id_tour)
    find_row.place(x = 950, y = 440)
    
    
def sales_page():
    
    if cursor is None:
        return
    
        
    def butt_add_to_sale():
        en.add_to_sale(cursor,cell_id_client_add.get(),cell_date_sale_add.get(),cell_id_employe_add.get()
                       ,cell_id_client_add.get(),cell_id_tour_add.get())

    def butt_find_row():
        en.search_sale_by_id(cursor,cell_id_sale_find.get())
        
    def butt_delete_sale():
        en.delete_sale_by_id(cursor,cell_id_sale_del.get())
        
    sales_page_r = Toplevel()
    sales_page_r.geometry('1200x750')
    button_font_up = tkFont.Font(family = "Times New Roman", size= 13)
    sales_page_r.title('Измение таблицы Продажи')
    Label(sales_page_r,text="id продажи", font=button_font_up).place(x = 63, y = 45)
    
    cell_id_sale_add = Entry(sales_page_r,width=170)
    cell_id_sale_add.place(x = 35, y = 95)

    Label(sales_page_r,text="дата\nпродажи", font=button_font_up).place(x = 260, y = 34)
    cell_date_sale_add = Entry(sales_page_r,width=170)
    cell_date_sale_add.place(x = 215, y = 95)
    
    Label(sales_page_r,text="количество\nпутевок", font=button_font_up).place(x = 425, y = 34)
    cell_quantity_sales_add = Entry(sales_page_r,width=170)
    cell_quantity_sales_add.place(x =396, y = 95)
    
    Label(sales_page_r,text="id клиента", font=button_font_up).place(x = 626, y = 45)
    cell_id_client_add = Entry(sales_page_r,width=170)
    cell_id_client_add.place(x = 577, y = 95)
    
    Label(sales_page_r,text="id сотрудника", font=button_font_up).place(x = 799, y = 45)
    cell_id_employe_add = Entry(sales_page_r,width=188)
    cell_id_employe_add.place(x = 776, y = 95)
    
    Label(sales_page_r,text="id тура", font=button_font_up).place(x = 1029, y = 45)
    cell_id_tour_add = Entry(sales_page_r,width=185)
    cell_id_tour_add.place(x = 972, y = 95)
    
    add_row = Button(sales_page_r,text='Добавить запись', font=button_font_up,command= butt_add_to_sale).place(x = 490, y = 165, width=220, height=45)
    ###
    

    Label(sales_page_r,text="id продажи", font=button_font_up).place(x = 85, y = 380)
    cell_id_sale_del = Entry(sales_page_r)
    cell_id_sale_del.place(x = 60, y = 427)
    

        
    delete_row = Button(sales_page_r,text = "Удалить данные" ,font = button_font_up,command=butt_delete_sale).place(x = 55, y = 502)
    
    show_table = Button(sales_page_r,text = "Вывести таблицу", font =button_font_up, command=show_sales_table ).place(x = 382, y = 410)
    show_table = Button(sales_page_r,text = "Очистить таблицу", font =button_font_up,command=en.clear_sale(cursor)).place(x = 620, y = 410)
    
    Label(sales_page_r,text="id продажи", font=button_font_up).place(x = 970 , y = 380)
    cell_id_sale_find = Entry(sales_page_r)
    cell_id_sale_find.place(x = 944, y = 427)
 ##доделать
 
           
    find_row = Button(sales_page_r,text = "Найти запись" ,font = button_font_up,command=butt_find_row).place(x = 951, y = 502)

def employees_page():
    
    if cursor is None:
        return
    
    def butt_add_to_employee():
        en.add_to_employee(cursor,cell_id_employee.get(),cell_full_name.get(),cell_phone.get(),cell_quantity_sales.get())
        
    def butt_find_row():
        en.search_employee_by_name(cursor,cell_id_employee_find.get())
    
    employees_page_r = Toplevel()
    employees_page_r.geometry("1200x750")
    button_font_up = tkFont.Font(family = "Times New Roman", size= 13)
    employees_page_r.title('Измение таблицы Сотрудники')
    
    Label(employees_page_r,text="id сотрудника", font=button_font_up).place(x = 66, y = 45)
    cell_id_employee = Entry(employees_page_r,width=195)
    cell_id_employee.place(x = 35, y = 95)
    
    Label(employees_page_r,text="ФИО", font=button_font_up).place(x = 430, y = 45)
    cell_full_name = Entry(employees_page_r,width=389)
    cell_full_name.place(x = 250, y = 95)

    Label(employees_page_r,text="количество\nпродаж", font=button_font_up).place(x = 745, y = 34)
    cell_quantity_sales = Entry(employees_page_r,width=258)
    cell_quantity_sales.place(x =662, y = 95)

    Label(employees_page_r,text="Номер телефона", font=button_font_up).place(x = 971, y = 45)
    cell_phone = Entry(employees_page_r,width=200)
    cell_phone.place(x = 943, y = 95)

    add_row = Button(employees_page_r,text='Добавить запись', font=button_font_up,
                     command=butt_add_to_employee).place(x = 490, y = 165, width=220, height=45)
    ###
   
    
    Label(employees_page_r,text="ФИО сотрудника", font=button_font_up).place(x = 70, y = 300)
    cell_id_employee_del = Entry(employees_page_r)
    cell_id_employee_del.place(x = 60, y = 347)
    
    def butt_delete_row():
        en.delete_employee_by_id(cursor,cell_id_employee_del.get())
    
    delete_row = Button(employees_page_r,text = "Удалить данные" ,font = button_font_up,command=butt_delete_row).place(x = 55, y = 422)
    
    show_table = Button(employees_page_r,text = "Вывести таблицу", font =button_font_up, command=show_employees_table).place(x = 382, y = 330)
    show_table = Button(employees_page_r,text = "Очистить таблицу", font =button_font_up,command=en.clear_employee(cursor)).place(x = 620, y = 330)
    
    Label(employees_page_r,text="ФИО сотрудника", font=button_font_up).place(x = 955 , y = 300)
    cell_id_employee_find = Entry(employees_page_r)
    cell_id_employee_find.place(x = 944, y = 347)
    #доделать
 
    find_row = Button(employees_page_r,text = "Найти запись" ,font = button_font_up,command=butt_find_row).place(x = 950, y = 422)

def clients_page(): 
    
    if cursor is None:
        return
    
    def butt_add_to_client():
     en.add_to_client(cursor,cell_id_client.get(),cell_full_name.get(),cell_passport.get(),cell_phone.get())   
     
    def butt_delete_row():
        en.delete_client_by_id(cursor,cell_id_client_del.get())
        
    def butt_delete_row():
        en.search_client_by_name(cursor,cell_full_name_find.get())
    
    clients_page_r = Toplevel()
    clients_page_r.geometry("1200x750")
    button_font_up = tkFont.Font(family = "Times New Roman", size= 13)
    clients_page_r.title('Измение таблицы Клиенты')
    
    Label(clients_page_r,text="id клиенты", font=button_font_up).place(x = 66, y = 45)
    cell_id_client = Entry(clients_page_r,width=195)
    cell_id_client.place(x = 35, y = 95)
    
    Label(clients_page_r,text="ФИО", font=button_font_up).place(x = 417, y = 45)
    cell_full_name = Entry(clients_page_r,width=389)
    cell_full_name.place(x = 250, y = 95)
    
    Label(clients_page_r,text="паспорт", font=button_font_up).place(x = 755, y = 45)
    cell_passport = Entry(clients_page_r,width=258)
    cell_passport.place(x =662, y = 95)
    
    Label(clients_page_r,text="номер телефона", font=button_font_up).place(x = 971, y = 45)
    cell_phone = Entry(clients_page_r,width=200)
    cell_phone.place(x = 943, y = 95)
    
    add_row = Button(clients_page_r,text='Добавить запись', font=button_font_up,
                     command=butt_add_to_client).place(x = 490, y = 165, width=220, height=45)
    ###
    
    
    Label(clients_page_r,text="id клиента", font=button_font_up).place(x = 90, y = 300)
    cell_id_client_del = Entry(clients_page_r,width=200)
    cell_id_client_del.place(x = 60, y = 347)
    

    
    delete_row = Button(clients_page_r,text = "Удалить данные" ,font = button_font_up,command=butt_delete_row).place(x = 55, y = 422)
    
    show_table = Button(clients_page_r,text = "Вывести таблицу", font =button_font_up, command=show_clients_table).place(x = 382, y = 330)
    show_table = Button(clients_page_r,text = "Очистить таблицу", font =button_font_up,command=en.clear_client(cursor)).place(x = 620, y = 330)
    
    Label(clients_page_r,text="ФИО", font=button_font_up).place(x = 990 , y = 300)
    
    cell_full_name_find = Entry(clients_page_r)
    cell_full_name_find.place(x = 944, y = 347)
    

    
    delete_row = Button(clients_page_r,text = "Найти запись" ,font = button_font_up,command=butt_delete_row).place(x = 950, y = 422)
    


    
    
home_page()

#loadimage = PhotoImage(file="button_show.png")
#show_tables = Button(image=loadimage,border=0)
#line_1 = Canvas()
#line_1.create_line(0,87,1200,87,width=3,fill="black")


