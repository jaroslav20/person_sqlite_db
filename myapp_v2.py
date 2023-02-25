import sqlite3
import random
import time
import sys
from datetime import date, timedelta


DB_NAME = 'myApp.db'    # Name database
NAME_WOMAN = 'name_w.txt'   # Filename with female names
NAME_MAN = 'name_m.txt'    # Filename with male names
NAME_MAN_F = 'name_m_f.txt'    # Filename with male names beginning with letter 'F'
NUMBER_OF_PEOPLE = 1000000     # Number of records generated


def create_table(conn, cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS people 
                      (full_name TEXT,
                       date_of_birth DATE,
                       gender TEXT)''')


def insert_data(conn, cursor, full_name, date_of_birth, gender):

    '''Insert records into database.'''

    cursor.execute('INSERT INTO people (full_name, date_of_birth, gender) VALUES (?, ?, ?)',
                   (full_name, date_of_birth, gender))


def select_man_f(conn, cursor):

    '''Select 100 male names that start with "F".'''

    rows = cursor.execute('''SELECT *
                          FROM people 
                          WHERE gender = "M" AND full_name LIKE "F%"
                          LIMIT 100;''')

    return cursor.fetchall()


def select_data(conn, cursor):

    '''Selects records from the database and calculates the age.'''

    cursor.execute('''SELECT DISTINCT full_name, date_of_birth, gender,
                      strftime('%Y', 'now') - strftime('%Y', date_of_birth) - (strftime('%m-%d', 'now') < strftime('%m-%d', date_of_birth)) AS age
                      FROM people
                      GROUP BY full_name || date_of_birth
                      ORDER BY full_name;''')
    return cursor.fetchall()


def get_values_in_bd(rows):

    '''Generates output to the console.'''

    for row in rows:
        if len(row) == 3:
            print(f'{row[0]} {row[1]} {row[2]}')
        elif len(row) == 4:
            print(f'{row[0]} {row[1]} {row[2]} {row[3]}')
        else:
            print("Database read error: string value not found")
    print(f"Total rows: {len(rows)}")


def opens_files_named():

    '''Opens files with names and immediately prescribes the appropriate gender.'''

    with open(NAME_MAN) as file_m:
        names_m = [{'name': line.rstrip(), 'gender': 'M'} for line in file_m]
    with open(NAME_WOMAN) as file_w:
        names_w = [{'name': line.rstrip(), 'gender': 'F'} for line in file_w]
    with open(NAME_MAN_F) as file_f:
        names_f = [{'name': line.rstrip(), 'gender': 'M'} for line in file_f]

    # Collect 100 names from the names_f list
    names_f = random.sample(names_f, 100)

    return names_m, names_w, names_f


def get_names_from_files():

    '''Forms a list of names and genders, then shuffles.'''

    names_m, names_w, names_f = opens_files_named()

    # Collect 100 names from the names_f list
    names_f_sample = random.sample(names_f, 100)

    # Combine the remaining names from names_f with names_m and names_w into a single list
    # remaining_f_names = [name for name in names_f if name not in names_f_sample]
    all_names = names_m + names_w + names_f_sample

    # Shuffle the combined list
    random.shuffle(all_names)

    return all_names


def generates_random_names_and_dates(conn, cursor):

    '''Takes again random names + gender and adds a random date of birth.
    Then calls the insert_data function.'''

    all_names = get_names_from_files()

    count = 0
    while count < NUMBER_OF_PEOPLE:
        random_names = random.choice(all_names)

        name = random_names['name']
        gender = random_names['gender']

        # Generate a random date between 80 and 12 years ago
        delta_days = random.randint(365 * 12, 365 * 80)
        dob = date.today() - timedelta(days=delta_days)

        # Adding records to the database
        insert_data(conn, cursor, name, dob, gender)

        count += 1
        if count >= NUMBER_OF_PEOPLE:
            break


def adding_one_entry(conn, cursor):

    '''Accepts a string from the user
    and converts it to values for insertion into the database.'''

    # Get string from user
    user_input = sys.stdin.readline().rstrip()

    # Getting values from a string
    lst_inp = user_input.split(' ')
    gender = f'{lst_inp[-1]}'
    dob = f'{lst_inp[-2]}'
    name = " ".join(lst_inp[:-2])

    # Adding the received values to the database
    insert_data(conn, cursor, name, dob, gender)
    print('The record was successfully added to the database')
    print(f'full name: {name}  date of birth: {dob} gender: {gender}')


def optimize(conn, cursor):
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_people_gender ON people (gender)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_people_fullname ON people (full_name)')


def main():

    '''Opens the database and executes all commands.'''

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        if len(sys.argv) > 1:
            command = sys.argv[1]
            if command == '1':
                create_table(conn, cursor)
            elif command == '2':
                adding_one_entry(conn, cursor)
            elif command == '3':
                rows = select_data(conn, cursor)
                get_values_in_bd(rows)
            elif command == '4':
                generates_random_names_and_dates(conn, cursor)
            elif command == '5':
                start_time = time.time()
                optimize(conn, cursor)
                rows_f = select_man_f(conn, cursor)
                get_values_in_bd(rows_f)
                end_time = time.time()
                print(f'Time taken: {end_time - start_time} seconds')

        conn.commit()


if __name__ == '__main__':
    main()