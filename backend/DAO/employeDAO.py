import psycopg2.extensions
import logging

from employe import Employe

class employeDAO:
    def __init__(self, db_connection: psycopg2.extensions.connection):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = db_connection
        self.logger = logging.getLogger("appLogger")

    def get_all_employees(self)-> list[Employe]:
        """
        Retrieve all employees from the database.
        :return: A list of Employee objects.
        """
        query = "SELECT * FROM employees"

        logging.debug("Retrieving all employees")

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
            
            logging.info(f"Retrieved {len(employees)} employees")
            return employees

    def get_employee_by_id(self, employee_id: int)-> Employe:
        """
        Retrieve an employee by their ID.
        :param employee_id: The ID of the employee to retrieve.
        :return: An Employee object.
        """
        query = "SELECT * FROM employees WHERE employeID = %s"

        logging.debug(f"Retrieving employee with ID: {employee_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employee_id,))
            row = cursor.fetchone()
            if row:
                return Employe(
                    employeeID=row[0],
                    rol=row[1]
                )
            else:
                self.logger.error(f"Employee with ID {employee_id} not found.")
                raise ValueError(f"Employee with ID {employee_id} not found.")

    def add_employee(self, employee: Employe)-> int:
        """
        Add a new employee to the database.
        :param employee: An Employee object to add.
        :return: The ID of the newly added employee.
        """
        query = "INSERT INTO employees (employeID, rol) VALUES (%s, %s)"
        
        logging.debug(f"Adding new employee: {employee}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employee.employeeID, employee.rol))

            self.db_connection.commit()
            logging.info(f"Employee added with ID: {employee.employeeID}")
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

        logging.debug(f"Updating employee with ID: {employe.employeeID}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employe.rol, employe.employeeID))

            self.db_connection.commit()
            logging.info(f"Employee updated with ID: {employe.employeeID}")
            return cursor.rowcount > 0
        
    def delete_employee(self, employee_id: int) -> bool:
        """
        Delete an employee from the database.
        :param employee_id: The ID of the employee to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        query = "DELETE FROM employees WHERE employeID = %s"

        logging.debug(f"Deleting employee with ID: {employee_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employee_id,))
            self.db_connection.commit()
            logging.info(f"Employee with ID {employee_id} deleted")
            return cursor.rowcount > 0
        
        