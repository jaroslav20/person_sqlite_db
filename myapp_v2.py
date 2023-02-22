import sqlite3
import random
import time
import sys
from datetime import datetime, timedelta


DB_NAME = 'myApp.db'
NAME_WOMAN = 'name_w.txt'
NAME_MAN = 'name_m.txt'
NAME_MAN_F = 'name_m_f.txt'



def create_table(conn, cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS people 
                      (full_name TEXT,
                       date_of_birth DATE,
                       gender TEXT)''')


def insert_data(conn, cursor, full_name, date_of_birth, gender):
    cursor.execute('INSERT INTO people (full_name, date_of_birth, gender) VALUES (?, ?, ?)',
                   (full_name, date_of_birth, gender))


def select_data(conn, cursor):
    cursor.execute('''SELECT full_name, date_of_birth, gender,
                      strftime('%Y', 'now') - strftime('%Y', date_of_birth) - (strftime('%m-%d', 'now') < strftime('%m-%d', date_of_birth)) AS age
                      FROM people
                      GROUP BY full_name || date_of_birth
                      ORDER BY full_name;''')
    return cursor.fetchall()


def fill_data(conn, cursor, num_records):
    names_m = [{'name': line.rstrip(), 'gender': 'M'} for line in open(NAME_MAN)]
    names_w = [{'name': line.rstrip(), 'gender': 'F'} for line in open(NAME_WOMAN)]
    choice_list = [names_m, names_w]

    for i in range(num_records):
        random_names = random.choice(choice_list)
        name = ''
        gender = ''
        for y in random_names:


            name = y['name']
            gender = y['gender']


        date_of_birth = datetime.now() - timedelta(days=random.randint(0, 365 * 60))
        insert_data(conn, cursor, name, date_of_birth, gender)



def optimize(conn, cursor):
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_people_gender ON people (gender)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_people_fullname ON people (full_name)')


def main():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        if len(sys.argv) > 1:
            command = sys.argv[1]
            if command == '1':
                create_table(conn, cursor)
            elif command == '2':
                name = sys.argv[2]
                dob = datetime.strptime(sys.argv[3], '%Y-%m-%d')
                gender = sys.argv[4]
                insert_data(conn, cursor, name, dob, gender)
            elif command == '3':
                rows = select_data(conn, cursor)
                for row in rows:
                    print(f'{row[0]} {row[1]} {row[2]} {row[3]}')
            elif command == '4':
                fill_data(conn, cursor, 1000000)
            elif command == '5':
                start_time = time.time()
                optimize(conn, cursor)
                rows = cursor.execute("SELECT * FROM people WHERE gender = 'M' AND full_name LIKE 'F%'").fetchall()
                end_time = time.time()
                for row in rows:
                    print(row)
                print(f'Time taken: {end_time - start_time} seconds')

        conn.commit()



if __name__ == '__main__':
    main()