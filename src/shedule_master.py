## MASTER FILE TO CALL ALL OTHER FUNCTIONALITIES

#Import employee script and Employee class
import employee as emp
from employee import Employee

import schedule

sample_data = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
]

employees = []
employees.append(Employee('Matthew Carroll', sample_data, 5))
employees.append(Employee('John Johnson', sample_data, 7))
employees.append(Employee('James Jameson', sample_data, 6))
employees.append(Employee('George Georgeson', sample_data, 4))
employees.append(Employee('Jenna Jennington', sample_data, 6))
employees.append(Employee('Sam Samuels', sample_data, 5))
employees.append(Employee('Charlie Charles', sample_data, 6))
employees.append(Employee('Tammy Tammuels', sample_data, 4))
emp.display_all()

schedule_info = schedule.create_table_schedule_info()
schedule.display_schedule_info()

week_schedule = schedule.create_week_schedule(employees)
schedule.display_week_schedule(week_schedule, employees)
schedule.remove_week_schedule(week_schedule)