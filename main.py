import psycopg2

# 1_Функция, создающая структуру БД (таблицы CUSTOMERS и PHONE_NUMBERS)
def create_table():
    conn = psycopg2.connect(host='localhost', database='customers_db', user='postgres', password='Khan781363!')
    with conn.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS customers(
                        client_id SERIAL PRIMARY KEY, 
                        client_name VARCHAR(30) NOT NULL,
                        surname VARCHAR(30) NOT NULL,
                        email VARCHAR(30) NOT NULL);''')
        cur.execute('''CREATE TABLE IF NOT EXISTS phone_numbers (
                        id_client INTEGER NOT NULL REFERENCES customers (client_id),
                        tel_number BIGINT UNIQUE NOT NULL);''')
        conn.commit()
    conn.close()
    print('Созданы таблицы customers, phone_numbers')


# 2_Функция, позволяющая добавить нового клиента.
def add_customer(name, surname, mail):
    conn = psycopg2.connect(host='localhost', database='customers_db', user='postgres', password='Khan781363!')
    with conn.cursor() as cur:
        cur.execute('''INSERT INTO customers (client_name, surname, email)
                            VALUES (%s, %s, %s);''', (name, surname, mail))

        print('Добавлен клиент: ', name, surname)
    conn.commit()
    conn.close()


# 3_Функция, позволяющая добавить телефон для существующего клиента.
def add_phone_number(name, surname, phone_numb):
    conn = psycopg2.connect(host='localhost', database='customers_db', user='postgres', password='Khan781363!')
    with conn.cursor() as cur:
        cur.execute('''SELECT client_id FROM customers c 
                    WHERE client_name = %s AND surname = %s;''', (name, surname))
        id_client_ = cur.fetchone()[0]
        cur.execute('''INSERT INTO phone_numbers (id_client, tel_number)
                                VALUES (%s, %s);''', (id_client_, phone_numb))
        print('Добавлен телефон для клинета : ', name, surname)
    conn.commit()
    conn.close()


# 4_Функция, позволяющая изменить данные о клиенте.
def change_data(name, surname, column, new_data):
    '''Функция принимает на вход 4 аргумента :
       имя клиента
       фамилия клиента
       название столбца, данные в котором нужно изменить
       новые данные'''
    conn = psycopg2.connect(host='localhost', database='customers_db', user='postgres', password='Khan781363!')
    with conn.cursor() as cur:
        cur.execute('''SELECT client_name , surname 
                       FROM customers ;''')
        customers_list = cur.fetchall()
        res = 0
        for man in customers_list:
            if name == man[0] and surname == man[1]:
                res = 1
                if column == 'client_name':
                    cur.execute('''UPDATE customers
                                    SET client_name = %s
                                WHERE client_id IN (SELECT client_id 
                                                        FROM customers c
                                                        WHERE client_name = %s AND surname = %s);''',
                                (new_data, name, surname))
                    print('Для клинета : ', name, surname, 'изменены данные: ', column)
                elif column == 'surname':
                    cur.execute('''UPDATE customers
                                    SET surname = %s
                                WHERE client_id IN (SELECT client_id 
                                                        FROM customers c
                                                        WHERE client_name = %s AND surname = %s);''',
                                (new_data, name, surname))
                    print('Для клинета : ', name, surname, 'изменены данные: ', column)
                elif column == 'email':
                    cur.execute('''UPDATE customers
                                    SET email = %s
                                WHERE client_id IN (SELECT client_id 
                                                        FROM customers c
                                                        WHERE client_name = %s AND surname = %s);''',
                                (new_data, name, surname))
                    print('Для клинета : ', name, surname, 'изменены данные: ', column)
                elif column == 'tel_number':
                    cur.execute('''UPDATE phone_numbers 
                                  SET tel_number  = %s
                                WHERE id_client  IN (SELECT client_id 
                                                       FROM customers
                                                      WHERE client_name = %s AND surname = %s);''',
                                (new_data, name, surname))
                    print('Для клинета : ', name, surname, 'изменены данные: ', column)
                else:
                    print('Колонка', column, 'отсутствует')
        if res == 0: print('Клиент', name, surname, 'отсутствует')
    conn.commit()
    conn.close()


# 5_Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone_number(name, surname):
    conn = psycopg2.connect(host='localhost', database='customers_db', user='postgres', password='Khan781363!')
    with conn.cursor() as cur:
        cur.execute('''DELETE FROM phone_numbers
                         WHERE id_client IN (SELECT client_id
                                               FROM customers c 
                                              WHERE client_name = %s AND surname = %s);''', (name, surname))
        print('Для клинета', name, surname, 'удалины все номера телефонов')
    conn.commit()
    conn.close()


# 6_Функция, позволяющая удалить существующего клиента.
def delete_customer(name, surname):
    conn = psycopg2.connect(host='localhost', database='customers_db', user='postgres', password='Khan781363!')
    with conn.cursor() as cur:
        cur.execute('''DELETE FROM phone_numbers
                         WHERE id_client IN (SELECT client_id 
                                               FROM customers c 
                                              WHERE client_name = %s AND surname = %s);''', (name, surname))
        cur.execute('''DELETE FROM customers 
                         WHERE client_id  IN (SELECT client_id 
                                                FROM customers c 
                                               WHERE client_name = %s AND surname = %s);''', (name, surname))
        print('Удален клинет', name, surname)
    conn.commit()
    conn.close()


# 7_Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def search_customer(data):
    conn = psycopg2.connect(host='localhost', database='customers_db', user='postgres', password='Khan781363!')

    with conn.cursor() as cur:
        cur.execute('''SELECT client_name , surname , email , tel_number
                            FROM customers c 
                            LEFT JOIN phone_numbers pn 
                            ON c.client_id  = pn.id_client ;''')
        customers_list = cur.fetchall()
        res = []
        for man in customers_list:
            if data in man:
                man = list(man)
                res.append(man)
        if len(res) == 0:
            print('По запросу', data, 'клиентов не найдено')
        else:
            print('По запросу', data, 'найдены :')
            for man in res:
                if man[3] == None: man[3] = 'Номер телефона не указан'
                print(man)
    conn.commit()
    conn.close()


# 8_Функция, позволяющая очистить таблицу
def clear_data(table):
    conn = psycopg2.connect(host='localhost', database='customers_db', user='postgres', password='Khan781363!')
    with conn.cursor() as cur:
        if table == 'phone_numbers':
            cur.execute('''DELETE FROM phone_numbers;''')
            print('Удалены все данные из таблицы phone_numbers')
        elif table == 'customers':
            cur.execute('''DELETE FROM customers;''')
            print('Удалены все данные из таблицы customers')
        else:
            print('Таблица', table, 'отсутствует')
    conn.commit()
    conn.close()


# 9_Функция, позволяющая удалить таблицу
def delete_table(table):
    conn = psycopg2.connect(host='localhost', database='customers_db', user='postgres', password='Khan781363!')
    with conn.cursor() as cur:
        if table == 'phone_numbers':
            cur.execute('''DROP TABLE phone_numbers;''')
            print('Удалена таблица phone_numbers')
        elif table == 'customers':
            cur.execute('''DROP TABLE customers;''')
            print('Удалена таблица customers')
        else:
            print('Таблица', table, 'отсутствует')
    conn.commit()
    conn.close()


# 1_Функция, создающая структуру БД (таблицы CUSTOMERS и PHONE_NUMBERS)
# create_table()
# Заполняем таблицу CUSTOMERS
list_customers = [('Rolan', 'Goros', 'r_goros@mail.ru'), ('Tim', 'Burton', 'burtontim@gmail.com'),
                  ('Orlando', 'Blum', 'orblum@mail.ru'), ('Emma', 'Watson', 'emma_wats@yandex.ru'),
                  ('Hulk', 'Alekseev', 'Aleks_hulk@mail.ru'), ('Rishak', 'Sanuk', 'rishsun@gmail.com'),
                  ('Andy', 'Ivanov', 'andy@mail.ru'), ('Tanos', 'Putanos', 'tanputan@yandex.ru'),
                  ('Gullia', 'Novars', 'novagul@mail.ru'), ('Dolce', 'Gabitov', 'dolcegab@yandex.ru'),
                  ('Victoria', 'Secret', 'vichka@mail.ru')]

# Заполняем таблицу phone_numbers
list_phone_numbers = [('Rolan', 'Goros', 89179174433), ('Tim', 'Burton', 89097654321), ('Orlando', 'Blum', 89651234567),
                      ('Emma', 'Watson', 89997776633), ('Hulk', 'Alekseev', 89098887766)]


