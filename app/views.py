from flask import Blueprint, request, jsonify
from .models import Employee
from . import db
from .tasks import find_highest, find_3_highest, sum_salary

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    return "Welcome to the Employee API"

@api_bp.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    new_employee = Employee(name=data['name'], salary=data['salary'], follow=data['follow'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee created successfully'}), 201

@api_bp.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result = [{'id': emp.id, 'name': emp.name, 'salary': emp.salary, 'follow': emp.follow} for emp in employees]
    return jsonify(result), 200

@api_bp.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    employee = Employee.query.get_or_404(id)
    employee.name = data.get('name', employee.name)
    employee.salary = data.get('salary', employee.salary)
    employee.follow = data.get('follow', employee.follow)
    db.session.commit()
    return jsonify({'message': 'Employee updated successfully'}), 200

@api_bp.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'}), 200

@api_bp.route('/find_employee_by_follow', methods=['POST'])
def find_employee_by_follow():
    data = request.get_json()
    follow_value = data.get('follow')
    
    if follow_value is None:
        return jsonify({'message': 'Follow value is required'}), 400
    
    task = find_highest.apply_async(args=[follow_value])
    result = task.get(timeout=10)

    return jsonify(result), 200

@api_bp.route('/total_salary_of_top_3_by_follow', methods=['POST'])
def total_salary_of_top_3_by_follow():
    data = request.get_json()
    follow_value = data.get('follow')
    
    if follow_value is None:
        return jsonify({'message': 'Follow value is required'}), 400
    
    # Task 1: Tìm ra 3 nhân viên có lương cao nhất theo follow
    task1 = find_3_highest.apply_async(args=[follow_value])
    top_employees = task1.get(timeout=10)

    if not top_employees:
        return jsonify({'message': 'No employees found for the given follow value'}), 404

    # Task 2: Tính tổng lương các nhân viên này
    task2 = sum_salary.apply_async(args=[top_employees])
    result = task2.get(timeout=10)

    # Xử lý kết quả từ task2
    if 'message' in result:
        return jsonify(result), 404
    
    return jsonify(result), 200

