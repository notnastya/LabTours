import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import datetime
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

# выделенный пользователь - viktor, пароль - viktor, он подключается к существующей базе данных
# база данных создается суперпользователем db_creator

file_open = open('create_drop_func.sql')
cr_dr_func = file_open.read()
file_open.close()

file_open = open('SQL-functions.sql')
func = file_open.read()
file_open.close()

engineURL = ''


def connect_as_creator(username_creator, password_creator, main_db, cr_dr_func):  # что это за main_db
    engine = create_engine(
        "postgresql+psycopg2://{}:{}@localhost/{}".format(username_creator, password_creator, main_db),
        echo=True)
    cursor = engine.connect()  # подключаемся
    cursor.execute(cr_dr_func)  # запускаем функции
    return cursor


def create_database(db_name, username,
                    cr_dr_func=cr_dr_func):  # название базы данных и имя пользователя, который будет ей пользоваться
    cursor = connect_as_creator('db_creator', 'db_creator', 'lab', cr_dr_func)
    cursor.execute('SELECT create_db(\'{}\', \'{}\')'.format(db_name, username))  # запускаем создание базы данных
    cursor.close()


# если в pgadmin подключаешься к базе, то от нее обязательно надо отключаться, чтобы дропалось
def drop_database(db_name, cr_dr_func=cr_dr_func):
    cursor = connect_as_creator('db_creator', 'db_creator', 'lab', cr_dr_func)
    cursor.execute('SELECT drop_db(\'{}\')'.format(db_name))  # запускаем удаление


def connect_as_user(username, password, db_name, functions=func):
    connection = psycopg2.connect(host='localhost', database=db_name, user=username, password=password)
    cursor = connection.cursor()
    cursor.execute(functions)
    connection.commit()
    return connection


def disconnect_user(connection):
    connection.close()


def clear_all_tables(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_all_tables()')
    connection.commit()


def clear_tour(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_tour()')
    connection.commit()


def clear_client(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_client()')
    connection.commit()


def clear_sale(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_sale()')
    connection.commit()


def clear_employee(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_employee()')
    connection.commit()


def show_table_sale(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT show_table_sale()')
    table = cursor.fetchall()
    return table


def show_table_tour(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT show_table_tour()')
    table = cursor.fetchall()
    return table


def show_table_employee(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT show_table_employee()')
    table = cursor.fetchall()
    return table


def show_table_client(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT show_table_client()')
    table = cursor.fetchall()
    return table

'''
def show_all_tables(connection):
    show_table_client(connection)
    show_table_sale(connection)
    show_table_employee(connection)
    show_table_tour(connection)
'''


def add_to_client(connection, v_id, v_name, v_passport, v_phone_number):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_client({}, \'{}\', {}, {})'.format(v_id, v_name, v_passport, v_phone_number))
    connection.commit()


def add_to_employee(connection, v_id, v_name, v_phone_number, v_sales_quantity):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_employee({}, \'{}\', {}, {})'.format(v_id, v_name, v_phone_number, v_sales_quantity))
    connection.commit()


def add_to_tour(connection, v_id, v_price, v_departure_date, v_departure_city, v_tour_operator, v_duration, v_country):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_tour({}, {}, \'{}\', \'{}\', \'{}\', {}, \'{}\')'.format(v_id, v_price, v_departure_date, v_departure_city,
                                                                           v_tour_operator, v_duration, v_country))
    connection.commit()


def add_to_sale(connection, v_id, v_sale_date, v_employee, v_client, v_tour ):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT add_to_sale( {}, \'{}\', {}, {}, {})'.format(v_id, v_sale_date, v_employee, v_client, v_tour))
    connection.commit()


def delete_client_by_name(connection, v_name):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_client_by_name(\'{}\')'.format(v_name))
    connection.commit()


def delete_client_by_id(connection, v_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_client_by_id({})'.format(v_id))
    connection.commit()


def delete_tour_by_id(connection, v_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_tour_by_id({})'.format(v_id))
    connection.commit()


def delete_employee_by_id(connection, v_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_employee_by_id({})'.format(v_id))
    connection.commit()


def delete_employee_by_name(connection, v_name):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_employee_by_name(\'{}\')'.format(v_name))
    connection.commit()


def delete_sale_by_id(connection, v_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_sale_by_id({})'.format(v_id))
    connection.commit()


def search_client_by_name(connection, client_name):
    cursor = connection.cursor()
    cursor.execute('SELECT search_client_by_name(\'{}\')'.format(client_name))
    table = cursor.fetchall()
    return table


def search_sale_by_id(connection, v_id):
    cursor = connection.cursor()
    cursor.execute('SELECT search_sale_by_id({})'.format(v_id))
    table = cursor.fetchall()
    return table


def search_tour_by_id(connection, v_id):
    cursor = connection.cursor()
    cursor.execute('SELECT search_tour_by_id({})'.format(v_id))
    table = cursor.fetchall()
    return table


def search_tour_by_country(connection, v_country):
    cursor = connection.cursor()
    cursor.execute('SELECT search_tour_by_country(\'{}\')'.format(v_country))
    table = cursor.fetchall()
    return table


def search_employee_by_id(connection, v_id):
    cursor = connection.cursor()
    cursor.execute('SELECT search_employee_by_id({})'.format(v_id))
    table = cursor.fetchall()
    return table


def search_employee_by_name(connection, v_name):
    cursor = connection.cursor()
    cursor.execute('SELECT search_employee_by_name(\'{}\')'.format(v_name))
    table = cursor.fetchall()
    return table


def update_tour(connection, v_id, v_price, v_departure_date, v_departure_city, v_tour_operator, v_duration, v_country):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT update_flower({}, {}, \'{}\', \'{}\',\'{}\', {}, \'{}\',)'.format(v_id, v_price, v_departure_date, v_departure_city, v_tour_operator, v_duration, v_country))
    connection.commit()



