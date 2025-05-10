import logging
from connect import get_db_connection

from DAO.employe import Employe

class EmployeDAO:
    def __init__(self):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        
        self.db_connection = get_db_connection()
        self.logger = logging.getLogger("appLogger")
    
    def get_all_employees(self)-> list[Employe]:
        """
        Retrieve all employees from the database.
        :return: A list of Employee objects.
        """
        query = """
                SELECT * FROM "Employes"
                """

        logging.debug("Retrieving all employees")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            employees = list[Employe]()
        
            for row in results:
                employee = Employe(
                    employe_id=row[0],
                    name=row[1],
                    family_name=row[2],
                    email=row[3],
                    rol=row[4]
                )
                employees.append(employee)
            
            logging.info(f"Retrieved {len(employees)} employees")
            return employees

    def get_employee_by_id(self, employe_id: str)-> Employe:
        """
        Retrieve an employee by their ID.
        :param employee_id: The ID of the employee to retrieve.
        :return: An Employee object.
        """
        query = """SELECT * FROM "Employes" WHERE "EmployeID" = %s"""

        logging.debug(f"Retrieving employee with ID: {employe_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employe_id,))
            row = cursor.fetchone()
            if row:
                return Employe(
                    employe_id=row[0],
                    name=row[1],
                    family_name=row[2],
                    email=row[3],
                    rol=row[4]
                )
            else:
                self.logger.error(f"Employee with ID {employe_id} not found.")
                raise ValueError(f"Employee with ID {employe_id} not found.")

    def add_employee(self, employe_id: str, name: str, family_name: str, email: str, rol: int = 0)-> Employe:
        """
        Add a new employee to the database.
        :param employe_id: The ID of the employee.
        :param name: The name of the employee.
        :param family_name: The family name of the employee.
        :param email: The email of the employee.
        :param rol: The role of the employee (default is 0).
        :return: The newly added employee.
        """
        query = """
        INSERT INTO "Employes" ("EmployeID", "Name", "Family_name", "Email", "Rol")
        VALUES (%s, %s, %s, %s, %s);
        """

        logging.debug(f"Adding employee with ID: {employe_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employe_id, name, family_name, email, rol))
            self.db_connection.commit()
            logging.info(f"Employee added with ID: {employe_id}")
            return Employe(employe_id=employe_id, name=name, family_name=family_name, email=email, rol=rol)
        
        
    def update_employee(self, employe_id: str, name: str, family_name: str, email: str, rol: int = 0)-> Employe:
        """
        Update an existing employee in the database.
        :param employe_id: The ID of the employee to update.
        :param name: The new name of the employee.
        :param family_name: The new family name of the employee.
        :param email: The new email of the employee.
        :param rol: The new role of the employee (default is 0).
        :return: The updated employee.
        """
        query = """
        UPDATE "Employes"
        SET "Name" = %s, "Family_name" = %s, "Email" = %s, "Rol" = %s
        WHERE "EmployeID" = %s;
        """

        logging.debug(f"Updating employee with ID: {employe_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (name, family_name, email, rol, employe_id))
            self.db_connection.commit()
            logging.info(f"Employee with ID {employe_id} updated")
            return Employe(employe_id=employe_id, name=name, family_name=family_name, email=email, rol=rol)
        
        
    def delete_employee(self, employee_id: int) -> bool:
        """
        Delete an employee from the database.
        :param employee_id: The ID of the employee to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        query = """DELETE FROM "Employes" WHERE "EmployeID" = %s"""

        logging.debug(f"Deleting employee with ID: {employee_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (employee_id,))
            self.db_connection.commit()
            logging.info(f"Employee with ID {employee_id} deleted")
            return cursor.rowcount > 0
        
        
    def retriveOrCreate(self, employe_id: str, name: str, family_name: str, email: str) -> Employe:
        """
        Create a new employee if they do not already exist in the database.
        :param employe: An Employee object to create.
        :return: True if the employee was created, False if they already exist.
        """
        try:
            return self.get_employee_by_id(employe_id)
        except ValueError:
            # Employee does not exist, proceed to create
            logging.debug(f"Employee with ID {employe_id} does not exist, creating new employee.")
            return self.add_employee(employe_id=employe_id, name=name, family_name=family_name, email=email)
        
        
