from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont
import engine as en

DB_NAME = 'lab_again'
USER_NAME = 'db_creator'
USER_PASSWORD = 'db_creator'

cursor = None



try:
    cursor = en.connect_as_user(USER_NAME, USER_PASSWORD, DB_NAME)
except:
    print('database does not exist')

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

def broken(root1):
    root1.title('database does not exist')
    button_font_up = tkFont.Font(family = "Courier New", size= 9)
    root1.geometry('200x250')
    root1['bg'] = 'RosyBrown1'
    w = root1.winfo_screenwidth()
    h = root1.winfo_screenheight()
    h = h//2
    w = w//2
    h = h - 150
    w = w - 130
    root1.geometry('200x250+{}+{}'.format(w,h))
    img = PhotoImage(file="cat.png")
    label = Label(root1, image=img)
    label.image_ref = img
    label.pack()
    label2 = Label(root1,text="something (or someone)\nis broken",font = button_font_up,bg='RosyBrown1').place(x = 20,y=210)
    root1.mainloop()

def home_page():
    root = Tk()
    root.title('БД Турагенства')
    root["bg"] = "RosyBrown1"
    
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w//2
    w = w - 600
    root.geometry('1200x750+{}+0'.format(w))
    

    button_font_up = tkFont.Font(family = "Courier New", size= 30)
    tours_button = Button(text = "Туры",font = button_font_up,bg ='light salmon' , command=tours_page,activeforeground = "deep pink",activebackground = 'white').place(x = 43, y = 127, width = 250, height = 100)
    clients_button = Button(text = "Клиенты",font = button_font_up,bg ='khaki1', command=clients_page,activeforeground = "deep pink").place(x = 334, y = 127, width = 250, height = 100)
    employees_button = Button(text = "Сотрудники",font = button_font_up,bg ='sky blue', command= employees_page,activeforeground = "deep pink").place(x = 625, y = 127, width = 250, height = 100)
    sales_button = Button(text = "Продажи",font = button_font_up,bg ='MediumPurple1', command= sales_page,activeforeground = "deep pink").place(x = 916, y = 127, width = 250, height = 100)

    button_font_down = tkFont.Font(family = "Courier New", size= 20)
    create_db = Button(text = "Создать базу данных",font = button_font_down,bg ='PaleGreen1' , command= create_database,activeforeground = "deep pink").place(x = 36, y = 462, width=350, height=120 )
    delete_db = Button(text = "Удалить базу данных",font = button_font_down,bg ='IndianRed1' ,command= delete_database,activeforeground = "deep pink").place(x = 781, y = 462, width=350, height=120 )
    show_tables = Button(text = "Вывести\nвсе таблицы",font = button_font_down,bd = 4,bg ='DodgerBlue2', command= show_all_table,activeforeground = "deep pink").place(x = 459, y = 471, width=250, height=100 )  
    root.mainloop()

def show_all_table():
    if cursor is None:
        root1 = Toplevel()
        broken(root1)
        return    
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
        print(values)
        values[0] = values[0][1:]
        values[3] = values[3][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3]))
  
    #[('(1,23000.00,2002-02-02,One,qweq,2,RTYU)',)]
    
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
    
    if cursor is None:
        root1 = Toplevel()
        broken(root1)
        return
    
    def butt_update_tour():
        en.update_tour(cursor,cell_id_ch.get(),cell_price_ch.get(),cell_data_tour_ch.get()
                        ,cell_departure_city_ch.get(),cell_tour_operator_ch.get(),cell_duration_ch.get(),cell_country_ch.get())

    def butt_add_to_tour():
        en.add_to_tour(cursor,cell_id_tour.get(),cell_price.get(),cell_data_tour.get(),
                       cell_departure_city.get(),cell_tour_operator.get(), cell_duration.get(),cell_country.get())

    def butt_delete_row():
        en.delete_tour_by_id(cursor,cell_id_tour_del.get())
        
    def butt_find_id_tour():
        en.search_tour_by_id(cell_id_tour_find.get())
    
    tours_page_r = Toplevel()
    w = tours_page_r.winfo_screenwidth()
    w = w//2
    w = w - 575
    tours_page_r.geometry('1150x700+{}+0'.format(w))
    #tours_page_r.geometry("1150x700")
    button_font_up = tkFont.Font(family = "Courier New", size= 13)
    tours_page_r.title('Измение таблицы Туры')
    tours_page_r['bg'] = 'RosyBrown1'
    
    label1=Label(tours_page_r,text="id тура", font=button_font_up,bg = "RosyBrown1").place(x = 62, y = 45)
    
    cell_id_tour = Entry(tours_page_r,width=157)
    cell_id_tour.place(x = 15, y = 95)
    
    label2 = Label(tours_page_r,text="цена", font=button_font_up,bg = "RosyBrown1").place(x = 240, y = 45)
    cell_price = Entry(tours_page_r,width=144)
    cell_price.place(x = 180, y = 95)
    
    labe3 = Label(tours_page_r,text="дата\nотправления", font=button_font_up,bg = "RosyBrown1").place(x = 370, y = 34)
    cell_data_tour = Entry(tours_page_r,width=160)
    cell_data_tour.place(x = 340, y = 95)

    label4 = Label(tours_page_r,text="город\nотправления", font=button_font_up,bg = "RosyBrown1").place(x = 530, y = 34)
    cell_departure_city = Entry(tours_page_r,width=144)
    cell_departure_city.place(x = 508, y = 95)
    
    label5 = Label(tours_page_r,text="тур\nоператор", font=button_font_up,bg = "RosyBrown1").place(x = 697, y = 34)
    cell_tour_operator = Entry(tours_page_r,width=156)
    cell_tour_operator.place(x = 661, y = 95)
    
    
    Label(tours_page_r,text="длительность\nтура", font=button_font_up,bg = "RosyBrown1").place(x = 841, y = 34)
    cell_duration = Entry(tours_page_r,width=154)
    cell_duration.place(x = 826, y = 95)
    
    Label(tours_page_r,text="страна", font=button_font_up,bg = "RosyBrown1").place(x = 1050, y = 45)
    cell_country = Entry(tours_page_r)
    cell_country.place(x = 999, y = 95)
    
    add_row = Button(tours_page_r,text='Добавить запись',bg ='light salmon', font=button_font_up, command=butt_add_to_tour).place(x = 450, y = 135, width=200, height=45)
    ###
    
    Label(tours_page_r,text="id тура", font=button_font_up,bg = "RosyBrown1").place(x = 62, y = 248)
    cell_id_ch = Entry(tours_page_r,width=157)
    cell_id_ch.place(x = 15, y = 296)
    
    Label(tours_page_r,text="цена", font=button_font_up,bg = "RosyBrown1").place(x = 240, y = 248)
    cell_price_ch = Entry(tours_page_r,width=144)
    cell_price_ch.place(x = 180, y = 296)

    Label(tours_page_r,text="дата\nотправления",bg = "RosyBrown1", font=button_font_up).place(x = 370, y = 241)
    cell_data_tour_ch = Entry(tours_page_r,width=160)
    cell_data_tour_ch.place(x =340, y = 296)
    
    Label(tours_page_r,text="город\nотправления",bg = "RosyBrown1", font=button_font_up).place(x = 530, y = 241)
    cell_departure_city_ch = Entry(tours_page_r,width=144)
    cell_departure_city_ch.place(x = 508, y = 296)
    
    Label(tours_page_r,text="тур\nоператор", font=button_font_up,bg = "RosyBrown1").place(x = 697, y = 241)
    cell_tour_operator_ch = Entry(tours_page_r,width=156)
    cell_tour_operator_ch.place(x = 661, y = 296)
    
    Label(tours_page_r,text="длительность\nтура", font=button_font_up,bg = "RosyBrown1").place(x = 841, y = 241)
    cell_duration_ch = Entry(tours_page_r,width=154)
    cell_duration_ch.place(x = 826, y = 296)

    Label(tours_page_r,text="страна", font=button_font_up,bg = "RosyBrown1").place(x = 1050, y = 241)
    cell_country_ch = Entry(tours_page_r)
    cell_country_ch.place(x = 999, y = 296)


    update_row = Button(tours_page_r,text='Обновить запись',bg ='light salmon', font=button_font_up,command= butt_update_tour).place(x = 450, y = 345, width=200, height=45)
    

    Label(tours_page_r,text="id тура", font=button_font_up,bg = "RosyBrown1").place(x = 70, y = 390)
    cell_id_tour_del = Entry(tours_page_r)
    cell_id_tour_del.place(x = 40, y = 430)
    
 
    
    delete_row = Button(tours_page_r,text = "Удалить данные" ,bg ='light salmon',font = button_font_up,command=butt_delete_row).place(x = 27, y = 470)
    
    show_table = Button(tours_page_r,text = "Вывести таблицу", bg ='light salmon',font =button_font_up, command=show_tours_table).place(x = 300, y = 450,width = 200 , height = 60)
    clear_table = Button(tours_page_r,text = "Очистить таблицу", bg ='light salmon',font =button_font_up,command=en.clear_tour(cursor)).place(x = 610, y = 450,width = 200 , height = 60)
    
    Label(tours_page_r,text="id тура", font=button_font_up,bg = "RosyBrown1").place(x = 970 , y = 390)
    cell_id_tour_find = Entry(tours_page_r)
    cell_id_tour_find.place(x = 944, y = 430)
    
    find_row = Button(tours_page_r,text = "Найти запись" ,font = button_font_up,bg ='light salmon', command=butt_find_id_tour)
    find_row.place(x = 942, y = 470)  
    
def sales_page():
    
    if cursor is None:
        root1 = Toplevel()
        broken(root1)
        return
        
    def butt_add_to_sale():
        en.add_to_sale(cursor,cell_id_client_add.get(),cell_date_sale_add.get(),cell_id_employe_add.get()
                       ,cell_id_client_add.get(),cell_id_tour_add.get())

    def butt_find_row():
        en.search_sale_by_id(cursor,cell_id_sale_find.get())
        
    def butt_delete_sale():
        en.delete_sale_by_id(cursor,cell_id_sale_del.get())
        
    sales_page_r = Toplevel()
    w = sales_page_r.winfo_screenwidth()
    w = w//2
    w = w - 575
    sales_page_r.geometry('1150x700+{}+0'.format(w))
    button_font_up = tkFont.Font(family = "Courier New", size= 13)
    button_font_big = tkFont.Font(family = "Courier New", size= 15)
    sales_page_r.title('Измение таблицы Продажи')
    sales_page_r['bg'] = 'RosyBrown1'
    
    Label(sales_page_r,text="id продажи", font=button_font_up,bg = "RosyBrown1").place(x = 63, y = 45)
    cell_id_sale_add = Entry(sales_page_r,width=170)
    cell_id_sale_add.place(x = 35, y = 95)

    Label(sales_page_r,text="дата\nпродажи", font=button_font_up,bg = "RosyBrown1").place(x = 260, y = 34)
    cell_date_sale_add = Entry(sales_page_r,width=170)
    cell_date_sale_add.place(x = 215, y = 95)
    
    Label(sales_page_r,text="количество\nпутевок", font=button_font_up,bg = "RosyBrown1").place(x = 425, y = 34)
    cell_quantity_sales_add = Entry(sales_page_r,width=170)
    cell_quantity_sales_add.place(x =396, y = 95)
    
    Label(sales_page_r,text="id клиента", font=button_font_up,bg = "RosyBrown1").place(x = 626, y = 45)
    cell_id_client_add = Entry(sales_page_r,width=170)
    cell_id_client_add.place(x = 577, y = 95)
    
    Label(sales_page_r,text="id сотрудника", font=button_font_up,bg = "RosyBrown1").place(x = 799, y = 45)
    cell_id_employe_add = Entry(sales_page_r,width=188)
    cell_id_employe_add.place(x = 776, y = 95)
    
    Label(sales_page_r,text="id тура", font=button_font_up,bg = "RosyBrown1").place(x = 1029, y = 45)
    cell_id_tour_add = Entry(sales_page_r,width=185)
    cell_id_tour_add.place(x = 972, y = 95)
    
    add_row = Button(sales_page_r,text='Добавить запись', font=button_font_up,bg ='MediumPurple1',command= butt_add_to_sale).place(x = 490, y = 165, width=220, height=45)
    

    Label(sales_page_r,text="id продажи", font=button_font_up,bg = "RosyBrown1").place(x = 70, y = 380)
    cell_id_sale_del = Entry(sales_page_r)
    cell_id_sale_del.place(x = 65, y = 427)
    
    delete_row = Button(sales_page_r,text = "Удалить данные" ,bg ='MediumPurple1',font = button_font_up,command=butt_delete_sale).place(x = 50, y = 480)
    
    show_table = Button(sales_page_r,text = "Вывести таблицу",bg ='MediumPurple1', font =button_font_big, command=show_sales_table ).place(x = 335, y = 280,width = 220 , height = 80)
    show_table = Button(sales_page_r,text = "Очистить таблицу",bg ='MediumPurple1', font =button_font_big,command=en.clear_sale(cursor)).place(x = 630, y = 280,width = 220 , height = 80)
    
    Label(sales_page_r,text="id продажи", font=button_font_up,bg = "RosyBrown1").place(x = 975 , y = 380)
    cell_id_sale_find = Entry(sales_page_r)
    cell_id_sale_find.place(x = 970, y = 427)
           
    find_row = Button(sales_page_r,text = "Найти запись" ,bg ='MediumPurple1',font = button_font_up,command=butt_find_row).place(x = 965, y = 480)

def employees_page():
    
    if cursor is None:
        root1 = Toplevel()
        broken(root1)
        return
    
    def butt_add_to_employee():
        en.add_to_employee(cursor,cell_id_employee.get(),cell_full_name.get(),cell_phone.get(),cell_quantity_sales.get())
        
    def butt_find_row():
        en.search_employee_by_name(cursor,cell_id_employee_find.get())
      
    def butt_delete_row():
        en.delete_employee_by_id(cursor,cell_id_employee_del.get())
    
    employees_page_r = Toplevel()
    w = employees_page_r.winfo_screenwidth()
    w = w//2
    w = w - 575
    employees_page_r.geometry('1150x700+{}+0'.format(w))
    button_font_up = tkFont.Font(family = "Courier New", size= 13)
    button_font_big = tkFont.Font(family = "Courier New", size= 15)
    employees_page_r.title('Измение таблицы Сотрудники')
    employees_page_r['bg'] = 'RosyBrown1'
    
    Label(employees_page_r,text="id сотрудника", font=button_font_up,bg = "RosyBrown1").place(x = 66, y = 45)
    cell_id_employee = Entry(employees_page_r,width=195)
    cell_id_employee.place(x = 35, y = 95)
    
    Label(employees_page_r,text="ФИО", font=button_font_up,bg = "RosyBrown1").place(x = 430, y = 45)
    cell_full_name = Entry(employees_page_r,width=389)
    cell_full_name.place(x = 250, y = 95)

    Label(employees_page_r,text="количество\nпродаж", font=button_font_up,bg = "RosyBrown1").place(x = 745, y = 34)
    cell_quantity_sales = Entry(employees_page_r,width=258)
    cell_quantity_sales.place(x =662, y = 95)

    Label(employees_page_r,text="Номер телефона", font=button_font_up,bg = "RosyBrown1").place(x = 971, y = 45)
    cell_phone = Entry(employees_page_r,width=200)
    cell_phone.place(x = 943, y = 95)

    add_row = Button(employees_page_r,text='Добавить запись',bg ='sky blue', font=button_font_up,
                     command=butt_add_to_employee).place(x = 490, y = 165, width=220, height=45)

    
    Label(employees_page_r,text="ФИО сотрудника", font=button_font_up,bg = "RosyBrown1").place(x = 60, y = 380)
    cell_id_employee_del = Entry(employees_page_r)
    cell_id_employee_del.place(x = 65, y = 427)
    
    delete_row = Button(employees_page_r,text = "Удалить данные" ,bg ='sky blue',font = button_font_up,command=butt_delete_row).place(x = 50, y = 480)
    
    show_table = Button(employees_page_r,text = "Вывести таблицу",bg ='sky blue', font =button_font_big, command=show_employees_table).place(x = 335, y = 280,width = 220 , height = 80)
    show_table = Button(employees_page_r,text = "Очистить таблицу",bg ='sky blue', font =button_font_big,command=en.clear_employee(cursor)).place(x = 630, y = 280,width = 220 , height = 80)
    
    Label(employees_page_r,text="ФИО сотрудника", font=button_font_up,bg = "RosyBrown1").place(x = 965 , y = 380)
    cell_id_employee_find = Entry(employees_page_r)
    cell_id_employee_find.place(x = 970, y = 427)
 
    find_row = Button(employees_page_r,text = "Найти запись" ,bg ='sky blue',font = button_font_up,command=butt_find_row).place(x = 965, y = 480)

def clients_page(): 
    
    if cursor is None:
        root1 = Toplevel()
        broken(root1)
        return
    
    def butt_add_to_client():
        en.add_to_client(cursor,cell_id_client.get(),cell_full_name.get(),cell_passport.get(),cell_phone.get())   
     
    def butt_delete_row():
        en.delete_client_by_id(cursor,cell_id_client_del.get())
        
    def butt_find_row():
        en.search_client_by_name(cursor,cell_full_name_find.get())
    
    clients_page_r = Toplevel()
    w = clients_page_r.winfo_screenwidth()
    w = w//2
    w = w - 575
    clients_page_r.geometry('1150x700+{}+0'.format(w))
    button_font_up = tkFont.Font(family = "Courier New", size= 13)
    clients_page_r.title('Измение таблицы Клиенты')
    clients_page_r["bg"] = "RosyBrown1"
    
    Label(clients_page_r,text="id клиенты", font=button_font_up,bg = "RosyBrown1").place(x = 75, y = 45)
    cell_id_client = Entry(clients_page_r,width=195)
    cell_id_client.place(x = 35, y = 95)
    
    Label(clients_page_r,text="ФИО", font=button_font_up,bg = "RosyBrown1").place(x = 430, y = 45)
    cell_full_name = Entry(clients_page_r,width=389)
    cell_full_name.place(x = 250, y = 95)
    
    Label(clients_page_r,text="паспорт", font=button_font_up,bg = "RosyBrown1").place(x = 755, y = 45)
    cell_passport = Entry(clients_page_r,width=258)
    cell_passport.place(x =662, y = 95)
    
    Label(clients_page_r,text="номер телефона", font=button_font_up,bg = "RosyBrown1").place(x = 971, y = 45)
    cell_phone = Entry(clients_page_r,width=200)
    cell_phone.place(x = 943, y = 95)
    
    add_row = Button(clients_page_r,text='Добавить запись', font=button_font_up,
                     command=butt_add_to_client,bg ='khaki1').place(x = 490, y = 165, width=220, height=45)
    
    
    Label(clients_page_r,text="id клиента", font=button_font_up,bg = "RosyBrown1").place(x = 70, y = 380)
    cell_id_client_del = Entry(clients_page_r)
    cell_id_client_del.place(x = 65, y = 427)
    delete_row = Button(clients_page_r,text = "Удалить данные",bg ='khaki1' ,font = button_font_up,command=butt_delete_row).place(x = 50, y = 480)
    
    show_table = Button(clients_page_r,text = "Вывести таблицу",bg ='khaki1', font =button_font_up, command=show_clients_table).place(x = 335, y = 280,width = 220 , height = 80)
    delete_table = Button(clients_page_r,text = "Очистить таблицу",bg ='khaki1', font =button_font_up,command=en.clear_client(cursor)).place(x = 630, y = 280,width = 220 , height = 80)
    
    Label(clients_page_r,text="ФИО", font=button_font_up,bg ='RosyBrown1').place(x = 1015, y = 380)
    cell_full_name_find = Entry(clients_page_r)
    cell_full_name_find.place(x = 970, y = 427)
    
    find_row = Button(clients_page_r,text = "Найти запись",bg ='khaki1' ,font = button_font_up,command=butt_find_row).place(x = 965, y = 480)
        
home_page()