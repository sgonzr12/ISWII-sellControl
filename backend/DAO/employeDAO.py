import psycopg2.extensions
from employe import Employe

class employeDAO:
    def __init__(self, db_connection: psycopg2.extensions.connection):
        self.db_connection = db_connection

    def get_all_employees(self)-> list[Employe]:
        """
        Retrieve all employees from the database.
        :return: A list of Employee objects.
        """
        query = "SELECT * FROM employees"
        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            employees = list[Employe]()
        
            for row in results:
                employee = Employe(
                    employeeID=row[0],
                    rol=row[1]
                )
                employees.append(employee)
        
            return employees

    def get_employee_by_id(self, employee_id: int)-> Employe:
        """
        Retrieve an employee by their ID.
        :param employee_id: The ID of the employee to retrieve.
        :return: An Employee object.
        """
        query = "SELECT * FROM employees WHERE employeID = %s"
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employee_id,))
            row = cursor.fetchone()
            if row:
                return Employe(
                    employeeID=row[0],
                    rol=row[1]
                )
            else:
                raise ValueError(f"Employee with ID {employee_id} not found.")

    def add_employee(self, employee: Employe)-> int:
        """
        Add a new employee to the database.
        :param employee: An Employee object to add.
        :return: The ID of the newly added employee.
        """
        
        query = "INSERT INTO employees (employeID, rol) VALUES (%s, %s)"
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employee.employeeID, employee.rol))
            self.db_connection.commit()
            return cursor.rowcount > 0
        
        
    def update_employee(self, employe: Employe) -> bool:
        """
        Update an existing employee in the database.
        :param employe: An Employee object with updated data.
        :return: True if the update was successful, False otherwise.
        """
        
        query = """
        UPDATE employees
        SET rol = %s
        WHERE employeID = %s;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employe.rol, employe.employeeID))
            self.db_connection.commit()
            return cursor.rowcount > 0
        
    def delete_employee(self, employee_id: int) -> bool:
        """
        Delete an employee from the database.
        :param employee_id: The ID of the employee to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        
        query = "DELETE FROM employees WHERE employeID = %s"
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employee_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        
        