import sqlite3
import datetime as dt

'''
GLOBAL METHODS
'''

#Schedule database file name
file = 'databases/schedule_db.db'

#Change data if shift necessities change
default_data = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [2, 2, 2],
    [2, 2, 2],
]

#Create schedule information table
def create_table_schedule_info():
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    #Do NOT change name
    table_name = 'schedule_info'

    #Check if database has already been created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        if table_name == table[0]:
            print('\nSchedule information already in database')
            return

    #Creates table to represent number of shifts needed for each day
    create_cmd = f'''CREATE TABLE {table_name}(
        needed_1 INTEGER,
        needed_2 INTEGER,
        needed_3 INTEGER
    )'''
    cursor.execute(create_cmd)

    #Insert shift data to database
    for item in default_data:
        cursor.execute(f"INSERT INTO {table_name} VALUES({item[0]},{item[1]},{item[2]})")
    conn.commit()
    print('\nCompant shift data added to database\n')

    return table_name

#Display schedule necessities
def display_schedule_info():
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    #Do NOT change name
    table_name = 'schedule_info'

    #Print shift necessities for the week
    print('\nNecessary shifts to be assigned for each day:\n')
    cursor.execute(f"SELECT * FROM {table_name}")
    schedule_info = cursor.fetchall()
    for item in range(len(schedule_info)):
        print('\t' + get_day(item) + ':')
        print(f'\t\t{get_shift_time(0)}: {str(schedule_info[item][0])}, {get_shift_time(1)}: {str(schedule_info[item][1])}, {get_shift_time(2)}: {str(schedule_info[item][2])}')

#Create schedule for the week starting next monday
def create_week_schedule(employee_list):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    today = dt.datetime.today()
    start_of_week = today + dt.timedelta((0 - today.weekday()) % 7)
    end_of_week = start_of_week + dt.timedelta(6)

    #Number of days in work week
    days_in_week = 7

    #Create schedule name based off start and end of week
    table_name = f'schedule_{start_of_week.strftime("%x")}_to_{end_of_week.strftime("%x")}'
    table_name = convert_to_underscore(table_name)

    #Check if this week's schedule already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        if table_name == table[0]:
            print(f'\n{table_name} already in database')
            return table_name
    
    #Create weekly schedule table
    create_cmd = f'''CREATE TABLE {table_name}(
        monday TEXT,
        tuesday TEXT,
        wednesday TEXT,
        thursday TEXT,
        friday TEXT,
        saturday TEXT,
        sunday TEXT
    )'''
    cursor.execute(create_cmd)
    print(f'\nCreated table {table_name}\n')

    #Initialize data structure for holding employee shift times
    employee_data = []
    for _ in employee_list:
        employee_data.append([-1, -1, -1, -1, -1, -1, -1])

    #Initialize shift data with days as columns and shifts as rows
    shift_data = []
    for x in range(len(default_data[0])):
        shift_data.append([default_data[0][x], default_data[1][x], default_data[2][x], default_data[3][x], default_data[4][x], default_data[5][x], default_data[6][x]])

    #Add employee to data list based on availability
    for shift in range(len(shift_data)):
        for day in range(len(shift_data[shift])):
            for emp in range(len(employee_list)):
                if (employee_list[emp].data[day][shift] == 1 and employee_list[emp].shifts_per_week > 0 and shift_data[shift][day] > 0):
                    employee_data[emp][day] = shift
                    shift_data[shift][day] -= 1
                    employee_list[emp].shifts_per_week -= 1
                    print(f'{employee_list[emp].name} scheduled for {get_day(day)}')

    #Finally insert shift data into this weeks data table
    for emp in employee_data:
        add_cmd = f"INSERT INTO {table_name} VALUES({emp[0]},{emp[1]},{emp[2]},{emp[3]},{emp[4]},{emp[5]},{emp[6]})"
        cursor.execute(add_cmd)
    conn.commit()

    return table_name

#Display schedule for the week
def display_week_schedule(name, employee_list):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    print(f'\n{name}:\n')
    cursor.execute(f"SELECT * FROM {name}")
    table_data = cursor.fetchall()
    for item in range(len(table_data)):
        print(f'\t{employee_list[item].name}:')
        print(f'\t\t{get_day(0)}: {get_shift_time(int(table_data[item][0]))},' 
            + f'\t{get_day(1)}: {get_shift_time(int(table_data[item][1]))},'
            + f'\t{get_day(2)}: {get_shift_time(int(table_data[item][2]))},'
            + f'\t{get_day(3)}: {get_shift_time(int(table_data[item][3]))},'
            + f'\t{get_day(4)}: {get_shift_time(int(table_data[item][4]))},'
            + f'\t{get_day(5)}: {get_shift_time(int(table_data[item][5]))},'
            + f'\t{get_day(6)}: {get_shift_time(int(table_data[item][6]))}')

#Remove schedule for a certain week
def remove_week_schedule(name):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    name = convert_to_underscore(name)

    remove_cmd = f"DROP TABLE {name}"
    cursor.execute(remove_cmd)
    print(f'\n{name} removed from database\n')

'''
HELPER METHODS
'''

#Get day from number of weekday
def get_day(num):
    if num == 0:
        return 'Monday'
    elif num == 1:
        return 'Tuesday'
    elif num == 2:
        return 'Wednesday'
    elif num == 3:
        return 'Thursday'
    elif num == 4:
        return 'Friday'
    elif num == 5:
        return 'Saturday'
    else:
        return 'Sunday'

#Get shift time from shift number
def get_shift_time(num):
    if num == 0:
        return '8AM-4PM'
    elif num == 1:
        return '10AM-6PM'
    elif num == 2:
        return '12PM-8PM'
    else:
        return 'No Shift'

#Convert schedule name for the week to have underscores (table names cannot have slashes)
def convert_to_underscore(name):
    return name.replace('/', '_')