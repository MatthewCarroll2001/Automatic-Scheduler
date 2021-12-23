import sqlite3

'''
CLASS
'''

#Class for instantiating an employee object
class Employee():

    name = ''
    data = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]
    shifts_per_week = 3

    #Creating an object automatically creates a database table
    def __init__(self, name, data, max_per_week):
        self.name = name
        self.data = data
        self.max_per_week = max_per_week

        create_table(name, data)

'''
GLOBAL METHODS
'''

#employee database file name
file = 'databases/employee_db.db'

#Create table for employee with name of employee as the name of the table
#Return name of employee
def create_table(name, data):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    name = convert_to_underscore(name)

    #Check if employee already exists in database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    emp_names = cursor.fetchall()
    for emp_name in emp_names:
        if name == emp_name[0]:
            print(f'{name} already in database')
            return

    #Create the table for the employee
    create_cmd = f'''CREATE TABLE {name}(
        shift_1 INTEGER,
        shift_2 INTEGER,
        shift_3 INTEGER
    )'''
    cursor.execute(create_cmd)

    #Add data for employee
    for day in data:
        cursor.execute(f"INSERT INTO {name} Values({day[0]},{day[1]},{day[2]})")
    conn.commit()    

    print(f'Created a table in the database for {convert_to_standard(name)}')

#Drop an employee from database
def remove_employee(name):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    name = convert_to_underscore(name)

    remove_cmd = f"DROP TABLE {name}"
    cursor.execute(remove_cmd)
    print(f'{name} removed from database')

#Drop all employees from database
def remove_all():
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = cursor.fetchall()
    for name in table_names:
        remove_employee(name[0])

#Display individual employee table
def display_employee(name):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    name = convert_to_underscore(name)

    print(f'\nShift data for {name}')
    cursor.execute(f"SELECT * FROM {name}")
    employee_data = cursor.fetchall()
    for data in employee_data:
        print(data)

#Display all employee tables
def display_all():
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    print('\nShift data for all employees:')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = cursor.fetchall()
    for name in table_names:
        print('\n\t' + convert_to_standard(name[0]) + ':')
        cursor.execute(f"SELECT * FROM {name[0]}")
        print('\t\t' + str(cursor.fetchall()))

'''
HELPER METHODS
'''

#Convert names so no spaces are present
def convert_to_underscore(name):
    return name.replace(' ', '_')

#Convert names back to having spaces for presentation
def convert_to_standard(name):
    return name.replace('_', ' ')