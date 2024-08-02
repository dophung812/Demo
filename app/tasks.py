from celery import Celery
from .models import Employee
from . import create_app, create_celery_app, db

app = create_app()
celery = create_celery_app(app)

# Tìm nhân viên có lương cao nhất theo follow
@celery.task
def find_highest(follow_value):
    employee = Employee.query.filter_by(follow=follow_value).order_by(Employee.salary.desc()).first()
    if employee:
        return [{'id': emp.id, 'name': emp.name, 'salary': emp.salary, 'follow': emp.follow} for emp in employee]
    else:
        return {'message': 'No employee'}

# Tìm 3 nhân viên có lương cao nhất theo follow
@celery.task
def find_3_highest(follow_value):
    employees = Employee.query.filter_by(follow=follow_value).order_by(Employee.salary.desc()).limit(3).all()
    return [{'id': emp.id, 'name': emp.name, 'salary': emp.salary, 'follow': emp.follow} for emp in employees]

@celery.task
def sum_salary(employee_data):
    if not employee_data:
        return {'message': 'No employees available for the given follow value'}
    total_salary = sum(emp['salary'] for emp in employee_data)
    return {'total_salary': total_salary}
