class Employe:
    def __init__(self, employeeID: int, rol: int):
        self.employeeID = employeeID
        
        if 1 <= rol <= 6:
            self.rol = rol
        else:
            raise ValueError("rol must be between 1 and 6")

    def __repr__(self):
        return f"Employee(employeeID={self.employeeID}, rol={self.rol})"